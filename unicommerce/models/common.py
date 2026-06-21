from pydantic import BaseModel


class ApiErrorDetail(BaseModel):
    code: int = 0
    message: str = ""
    description: str = ""


class ApiWarning(BaseModel):
    code: int = 0
    message: str = ""
    description: str = ""
