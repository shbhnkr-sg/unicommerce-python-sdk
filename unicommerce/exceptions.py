class UnicommerceError(Exception):
    pass


class AuthenticationError(UnicommerceError):
    pass


class AuthorizationError(UnicommerceError):
    pass


class ValidationError(UnicommerceError):
    def __init__(self, message: str, errors: list[dict] | None = None):
        super().__init__(message)
        self.errors = errors or []


class RateLimitError(UnicommerceError):
    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class ApiError(UnicommerceError):
    def __init__(
        self,
        message: str,
        code: int = 0,
        errors: list[dict] | None = None,
        warnings: list[dict] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.errors = errors or []
        self.warnings = warnings or []


class ServerError(UnicommerceError):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code


class NetworkError(UnicommerceError):
    pass


class TimeoutError(UnicommerceError):
    pass
