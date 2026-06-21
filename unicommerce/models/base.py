from pydantic import BaseModel, ConfigDict, PrivateAttr


class UnicommerceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class UnicommerceResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    _raw: dict = PrivateAttr(default_factory=dict)

    @property
    def raw(self) -> dict:
        return self._raw
