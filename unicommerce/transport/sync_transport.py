from __future__ import annotations

import time

import httpx
from pydantic import BaseModel

from unicommerce._logging import logger
from unicommerce.exceptions import (
    AuthenticationError,
    NetworkError,
)
from unicommerce.exceptions import (
    TimeoutError as UCTimeoutError,
)
from unicommerce.models.pdf import PdfResponse
from unicommerce.transport.base import BaseTransport


class SyncTransport(BaseTransport):
    def __init__(self, config, auth):
        super().__init__(config, auth)
        self._client = httpx.Client(timeout=config.timeout)

    def request(
        self,
        path: str,
        body: BaseModel | dict | None = None,
        response_model=None,
        facility: str | None = None,
        safe_to_retry: bool = False,
        dto_key: str | None = None,
    ):
        last_error: Exception | None = None
        auth_retried = False

        for attempt in range(self.config.max_retries + 1):
            try:
                token = self._auth.get_token_sync()
                headers = self._build_headers(token, facility)
                url = self._build_url(path)

                json_body = None
                if body is not None:
                    json_body = (
                        body.model_dump(by_alias=True, exclude_none=True)
                        if isinstance(body, BaseModel)
                        else body
                    )

                response = self._client.post(url, json=json_body, headers=headers)
                data = response.json()

                logger.debug("POST %s -> %d (attempt %d)", path, response.status_code, attempt + 1)

                return self._parse_response(
                    response.status_code, data, response_model, headers=dict(response.headers), dto_key=dto_key
                )

            except AuthenticationError:
                if not auth_retried:
                    auth_retried = True
                    self._auth.force_refresh_sync()
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
                logger.warning("Retrying %s (attempt %d) after %.2fs", path, attempt + 1, delay)
                time.sleep(delay)
            elif last_error:
                raise last_error

        raise last_error  # type: ignore

    def get_pdf(
        self,
        path: str,
        params: dict,
        facility: str | None = None,
    ) -> PdfResponse:
        token = self._auth.get_token_sync()
        headers = self._build_headers(token, facility)
        headers.pop("Content-Type", None)
        url = self._build_url(path)

        response = self._client.get(url, params=params, headers=headers)

        if response.status_code == 401:
            self._auth.force_refresh_sync()
            token = self._auth.get_token_sync()
            headers["Authorization"] = f"Bearer {token}"
            response = self._client.get(url, params=params, headers=headers)

        if response.status_code != 200:
            self._parse_response(response.status_code, response.json(), None)

        return PdfResponse(response.content)

    def close(self):
        self._client.close()
