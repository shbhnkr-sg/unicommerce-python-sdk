from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UnicommerceConfig:
    tenant: str
    username: str
    password: str
    client_id: str = "my-trusted-client"
    facility: str | None = None
    timeout: float = 30.0
    max_retries: int = 3
    retry_base_delay: float = 0.5
    retry_max_delay: float = 8.0
    token_refresh_buffer: int = 60

    @property
    def base_url(self) -> str:
        return f"https://{self.tenant}.unicommerce.com"
