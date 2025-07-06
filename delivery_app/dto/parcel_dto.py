from enum import Enum
from typing import Optional, Union

from pydantic import field_serializer

from dto.base_dto import BaseSchema


class ParcelTypeEnum(str, Enum):
    clothes = "clothes"
    electronics = "electronics"
    miscellaneous = "miscellaneous"


class ParcelDTO(BaseSchema):
    parcel_id: str
    name: str
    weight: float
    parcel_type: ParcelTypeEnum
    content_value_usd: float

    delivery_cost_rub: Optional[float | str]

    @field_serializer("delivery_cost_rub", return_type=Union[float, str])
    def serialize_delivery_cost_rub(self, value):
        return value if value is not None else "Not calculated"


class ParcelsDTO(BaseSchema):
    parcels: list[ParcelDTO | None]


class ParcelTypeDTO(BaseSchema):
    id: int
    name: str


class ParcelTypesDTO(BaseSchema):
    parcel_types: list[ParcelTypeDTO]
