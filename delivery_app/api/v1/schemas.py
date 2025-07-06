from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_serializer


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


class ParcelID(BaseSchema):
    parcel_id: str


class ParcelOut(ParcelCreated):
    delivery_cost_rub: Optional[float | str]

    @field_serializer("delivery_cost_rub", return_type=Union[float, str])
    def serialize_delivery_cost_rub(self, value):
        return value if value is not None else "Not calculated"


class Parcels(BaseSchema):
    parcels: list[ParcelOut | None]


class ParcelType(BaseSchema):
    id: int
    name: str


class ParcelTypes(BaseSchema):
    parcel_types: list[ParcelType]


class StatisticsOut(BaseSchema):
    date: str
    parcel_type: str
    total_cost: float


class DailyStatisticsResponse(BaseModel):
    data: list[StatisticsOut]
