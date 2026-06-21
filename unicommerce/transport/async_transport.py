from __future__ import annotations

import asyncio

import httpx
from pydantic import BaseModel

from unicommerce.transport.base import BaseTransport
from unicommerce.exceptions import (
    AuthenticationError,
    NetworkError,
    TimeoutError as UCTimeoutError,
)
from unicommerce._logging import logger


class AsyncTransport(BaseTransport):
    def __init__(self, config, auth):
        super().__init__(config, auth)
        self._client = httpx.AsyncClient(timeout=config.timeout)

    async def request(
        self,
        path: str,
        body: BaseModel | dict | None = None,
        response_model=None,
        facility: str | None = None,
        safe_to_retry: bool = False,
    ):
        last_error = None
        auth_retried = False

        for attempt in range(self.config.max_retries + 1):
            try:
                token = await self._auth.get_token()
                headers = self._build_headers(token, facility)
                url = self._build_url(path)

                json_body = None
                if body is not None:
                    json_body = (
                        body.model_dump(by_alias=True, exclude_none=True)
                        if isinstance(body, BaseModel)
                        else body
                    )

                response = await self._client.post(url, json=json_body, headers=headers)
                data = response.json()

                logger.debug(
                    "POST %s -> %d (attempt %d)", path, response.status_code, attempt + 1
                )

                return self._parse_response(
                    response.status_code, data, response_model, headers=dict(response.headers)
                )

            except AuthenticationError:
                if not auth_retried:
                    auth_retried = True
                    await self._auth.force_refresh()
                    continue
                raise
            except httpx.TimeoutException as e:
                last_error = UCTimeoutError(str(e))
            except httpx.NetworkError as e:
                last_error = NetworkError(str(e))
            except (NetworkError, UCTimeoutError) as e:
                last_error = e
            except Exception as e:
                if self._should_retry(e, attempt, safe_to_retry):
                    last_error = e
                else:
                    raise

            if last_error and self._should_retry(last_error, attempt, safe_to_retry):
                delay = self._compute_backoff(attempt)
                logger.warning(
                    "Retrying %s (attempt %d) after %.2fs", path, attempt + 1, delay
                )
                await asyncio.sleep(delay)
            elif last_error:
                raise last_error

        raise last_error  # type: ignore

    async def close(self):
        await self._client.aclose()
