from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(alias="access_token")
    token_type: str = Field(alias="token_type")
    refresh_token: str = Field(alias="refresh_token")
    expires_in: int = Field(alias="expires_in")
    scope: str = ""
