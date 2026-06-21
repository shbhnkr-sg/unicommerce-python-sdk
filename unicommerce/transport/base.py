from __future__ import annotations

from unicommerce.config import UnicommerceConfig
from unicommerce.auth import AuthManager
from unicommerce.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    NetworkError,
    RateLimitError,
    ServerError,
    TimeoutError as UCTimeoutError,
    ValidationError,
)
from unicommerce._retry import compute_backoff


class BaseTransport:
    def __init__(self, config: UnicommerceConfig, auth: AuthManager) -> None:
        self.config = config
        self._auth = auth

    def _build_url(self, path: str) -> str:
        return f"{self.config.base_url}/services/rest/v1{path}"

    def _build_headers(self, token: str, facility: str | None) -> dict:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        effective_facility = facility or self.config.facility
        if effective_facility:
            headers["Facility"] = effective_facility
        return headers

    def _parse_response(self, status_code: int, data: dict, response_model: type | None, headers: dict | None = None):
        if status_code == 401:
            raise AuthenticationError("Authentication failed")
        if status_code == 403:
            raise AuthorizationError("Authorization failed")
        if status_code == 429:
            retry_after = None
            if headers and "retry-after" in headers:
                try:
                    retry_after = float(headers["retry-after"])
                except (ValueError, TypeError):
                    pass
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if status_code == 400:
            errors = data.get("errors", [])
            message = data.get("message", "Validation error")
            raise ValidationError(message, errors=errors)
        if 500 <= status_code <= 599:
            raise ServerError(f"Server error: {status_code}", status_code=status_code)

        # Check for logical API failure on 200
        if data.get("successful") is False:
            raise ApiError(
                message=data.get("message", "API request failed"),
                code=data.get("code", 0),
                errors=data.get("errors", []),
                warnings=data.get("warnings", []),
            )

        if response_model is None:
            return data

        # Validate into response model
        model = response_model.model_validate(data)
        model._raw = data
        return model

    def _should_retry(self, error: Exception, attempt: int, safe_to_retry: bool) -> bool:
        if attempt >= self.config.max_retries:
            return False
        if isinstance(error, (NetworkError, UCTimeoutError)):
            return safe_to_retry
        if isinstance(error, ServerError) and error.status_code in (502, 503, 504):
            return safe_to_retry
        if isinstance(error, RateLimitError):
            return safe_to_retry
        return False

    def _compute_backoff(self, attempt: int) -> float:
        return compute_backoff(
            attempt,
            base=self.config.retry_base_delay,
            cap=self.config.retry_max_delay,
        )
