from pydantic import BaseModel, ConfigDict


class PartyTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class BillTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class UnitResponse(BaseModel):
    id: int
    unit_code: str
    unit_name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class DeductionTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class TaxTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )