from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NewParcel(BaseSchema):
    name: str
    weight: float
    parcel_type: str
    content_value_usd: float


class ParcelCreated(NewParcel):
    parcel_id: str


class ParcelOut(ParcelCreated):
    delivery_cost_rub: str | float


class Parcels(BaseSchema):
    parcels: list[ParcelOut]


class ParcelTypes(BaseSchema):
    pass
