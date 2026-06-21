from __future__ import annotations

import asyncio
import threading
import time

import httpx

from unicommerce.config import UnicommerceConfig
from unicommerce._logging import logger


class AuthManager:
    def __init__(self, config: UnicommerceConfig) -> None:
        self._config = config
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._expires_at: float = 0.0
        self._async_lock = asyncio.Lock()
        self._sync_lock = threading.Lock()

    def _is_token_valid(self) -> bool:
        return (
            self._access_token is not None
            and time.monotonic() < self._expires_at - self._config.token_refresh_buffer
        )

    def _do_password_grant(self, client: httpx.Client | httpx.AsyncClient) -> dict:
        url = (
            f"{self._config.base_url}/oauth/token"
            f"?grant_type=password"
            f"&client_id={self._config.client_id}"
            f"&username={self._config.username}"
            f"&password={self._config.password}"
        )
        response = client.get(url)
        response.raise_for_status()
        return response.json()

    def _do_refresh_grant(self, client: httpx.Client | httpx.AsyncClient, refresh_token: str) -> dict:
        url = (
            f"{self._config.base_url}/oauth/token"
            f"?grant_type=refresh_token"
            f"&client_id={self._config.client_id}"
            f"&refresh_token={refresh_token}"
        )
        response = client.get(url)
        response.raise_for_status()
        return response.json()

    def _store_token(self, data: dict) -> None:
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        self._expires_at = time.monotonic() + data["expires_in"]
        logger.debug("Token stored, expires in %d seconds", data["expires_in"])

    # --- Async methods ---

    async def _async_password_grant(self) -> dict:
        async with httpx.AsyncClient(timeout=self._config.timeout) as client:
            url = (
                f"{self._config.base_url}/oauth/token"
                f"?grant_type=password"
                f"&client_id={self._config.client_id}"
                f"&username={self._config.username}"
                f"&password={self._config.password}"
            )
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def _async_refresh_grant(self, refresh_token: str) -> dict:
        async with httpx.AsyncClient(timeout=self._config.timeout) as client:
            url = (
                f"{self._config.base_url}/oauth/token"
                f"?grant_type=refresh_token"
                f"&client_id={self._config.client_id}"
                f"&refresh_token={refresh_token}"
            )
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def get_token(self) -> str:
        if self._is_token_valid():
            return self._access_token  # type: ignore

        async with self._async_lock:
            # Double-check after acquiring lock
            if self._is_token_valid():
                return self._access_token  # type: ignore

            # Try refresh first if we have a refresh token
            if self._refresh_token is not None:
                try:
                    data = await self._async_refresh_grant(self._refresh_token)
                    self._store_token(data)
                    return self._access_token  # type: ignore
                except (httpx.HTTPStatusError, httpx.HTTPError):
                    logger.debug("Refresh grant failed, falling back to password grant")

            # Fall back to password grant
            data = await self._async_password_grant()
            self._store_token(data)
            return self._access_token  # type: ignore

    async def force_refresh(self) -> str:
        async with self._async_lock:
            if self._refresh_token is not None:
                try:
                    data = await self._async_refresh_grant(self._refresh_token)
                    self._store_token(data)
                    return self._access_token  # type: ignore
                except (httpx.HTTPStatusError, httpx.HTTPError):
                    logger.debug("Refresh grant failed during force_refresh, falling back to password grant")

            data = await self._async_password_grant()
            self._store_token(data)
            return self._access_token  # type: ignore

    # --- Sync methods ---

    def get_token_sync(self) -> str:
        if self._is_token_valid():
            return self._access_token  # type: ignore

        with self._sync_lock:
            # Double-check after acquiring lock
            if self._is_token_valid():
                return self._access_token  # type: ignore

            # Try refresh first if we have a refresh token
            if self._refresh_token is not None:
                try:
                    with httpx.Client(timeout=self._config.timeout) as client:
                        data = self._do_refresh_grant(client, self._refresh_token)
                        self._store_token(data)
                        return self._access_token  # type: ignore
                except (httpx.HTTPStatusError, httpx.HTTPError):
                    logger.debug("Refresh grant failed, falling back to password grant")

            # Fall back to password grant
            with httpx.Client(timeout=self._config.timeout) as client:
                data = self._do_password_grant(client)
                self._store_token(data)
                return self._access_token  # type: ignore

    def force_refresh_sync(self) -> str:
        with self._sync_lock:
            if self._refresh_token is not None:
                try:
                    with httpx.Client(timeout=self._config.timeout) as client:
                        data = self._do_refresh_grant(client, self._refresh_token)
                        self._store_token(data)
                        return self._access_token  # type: ignore
                except (httpx.HTTPStatusError, httpx.HTTPError):
                    logger.debug("Refresh grant failed during force_refresh_sync, falling back to password grant")

            with httpx.Client(timeout=self._config.timeout) as client:
                data = self._do_password_grant(client)
                self._store_token(data)
                return self._access_token  # type: ignore
