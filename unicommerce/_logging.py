import logging
import re

logger = logging.getLogger("unicommerce")

_REDACT_PATTERNS = [
    re.compile(
        r"(password|access_token|refresh_token|authorization)[\"']?\s*[:=]\s*[\"']?[^\s,\"'}\]]+",
        re.IGNORECASE,
    ),
]

_REDACT_KEYS = frozenset(
    {
        "password",
        "access_token",
        "refresh_token",
        "authorization",
        "phone",
        "email",
        "addressLine1",
        "addressLine2",
    }
)


def redact_dict(data: dict) -> dict:
    return {k: "***REDACTED***" if k.lower() in _REDACT_KEYS else v for k, v in data.items()}


def redact_string(text: str) -> str:
    result = text
    for pattern in _REDACT_PATTERNS:
        result = pattern.sub(
            lambda m: (
                m.group().split(":", 1)[0] + ": ***REDACTED***"
                if ":" in m.group()
                else m.group().split("=", 1)[0] + "=***REDACTED***"
            ),
            result,
        )
    return result
