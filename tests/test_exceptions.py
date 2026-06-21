from unicommerce.exceptions import (
    ApiError,
    AuthenticationError,
    AuthorizationError,
    NetworkError,
    RateLimitError,
    ServerError,
    TimeoutError,
    UnicommerceError,
    ValidationError,
)


def test_hierarchy():
    assert issubclass(AuthenticationError, UnicommerceError)
    assert issubclass(AuthorizationError, UnicommerceError)
    assert issubclass(ValidationError, UnicommerceError)
    assert issubclass(RateLimitError, UnicommerceError)
    assert issubclass(ApiError, UnicommerceError)
    assert issubclass(ServerError, UnicommerceError)
    assert issubclass(NetworkError, UnicommerceError)
    assert issubclass(TimeoutError, UnicommerceError)


def test_api_error_attributes():
    err = ApiError("bad request", code=1001, errors=[{"field": "sku"}], warnings=[{"msg": "deprecated"}])
    assert err.code == 1001
    assert err.errors == [{"field": "sku"}]
    assert err.warnings == [{"msg": "deprecated"}]
    assert str(err) == "bad request"


def test_validation_error_attributes():
    err = ValidationError("invalid", errors=[{"field": "qty", "msg": "must be positive"}])
    assert err.errors == [{"field": "qty", "msg": "must be positive"}]


def test_rate_limit_error_attributes():
    err = RateLimitError("too many requests", retry_after=30.0)
    assert err.retry_after == 30.0


def test_server_error_attributes():
    err = ServerError("internal error", status_code=502)
    assert err.status_code == 502


def test_catch_all():
    try:
        raise AuthenticationError("token expired")
    except UnicommerceError as e:
        assert str(e) == "token expired"
