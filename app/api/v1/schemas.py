from enum import Enum

from pydantic import BaseModel, ConfigDict


class ParcelTypeEnum(str, Enum):
    clothes = "clothes"
    electronics = "electronics"
    miscellaneous = "miscellaneous"


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NewParcel(BaseSchema):
    name: str
    weight: float
    parcel_type: ParcelTypeEnum
    content_value_usd: float


class ParcelCreated(NewParcel):
    parcel_id: str


class ParcelOut(ParcelCreated):
    delivery_cost_rub: str | float


class Parcels(BaseSchema):
    parcels: list[ParcelOut | None]


class ParcelType(BaseSchema):
    id: int
    name: str


class ParcelTypes(BaseSchema):
    pacel_types: list[ParcelType]
