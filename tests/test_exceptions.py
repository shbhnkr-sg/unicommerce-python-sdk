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


def test_all_exceptions_inherit_from_base():
    assert issubclass(AuthenticationError, UnicommerceError)
    assert issubclass(AuthorizationError, UnicommerceError)
    assert issubclass(ValidationError, UnicommerceError)
    assert issubclass(RateLimitError, UnicommerceError)
    assert issubclass(ApiError, UnicommerceError)
    assert issubclass(ServerError, UnicommerceError)
    assert issubclass(NetworkError, UnicommerceError)
    assert issubclass(TimeoutError, UnicommerceError)


def test_api_error_carries_attributes():
    err = ApiError("bad", code=1001, errors=[{"field": "sku"}], warnings=[])
    assert err.code == 1001
    assert err.errors == [{"field": "sku"}]
    assert str(err) == "bad"


def test_catch_all_with_base_class():
    try:
        raise AuthenticationError("expired")
    except UnicommerceError as e:
        assert str(e) == "expired"
