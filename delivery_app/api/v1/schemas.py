from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class ParcelTypeEnum(str, Enum):
    clothes = "clothes"
    electronics = "electronics"
    miscellaneous = "miscellaneous"


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NewParcel(BaseSchema):
    name: str = Field(..., min_length=3, max_length=255)
    weight: float = Field(..., gt=0)
    parcel_type: ParcelTypeEnum = Field(...)
    content_value_usd: float = Field(..., gt=0)

    @field_validator("name")
    def name_must_be_alphanumeric(cls, v):
        if not v.replace(" ", "").isalnum():
            raise ValueError("name has to contain letters or digitals")
        return v


class ParcelCreated(NewParcel):
    parcel_id: str = Field(...)


class ParcelID(BaseSchema):
    parcel_id: str = Field(...)


class ParcelOut(ParcelCreated):
    delivery_cost_rub: Optional[float | str] = Field(default="Not calculated")

    @field_serializer("delivery_cost_rub", return_type=Union[float, str])
    def serialize_delivery_cost_rub(self, value):
        return value if value is not None else "Not calculated"


class Parcels(BaseSchema):
    parcels: list[ParcelOut | None] = Field(...)


class ParcelType(BaseSchema):
    id: int = Field(..., gt=0)
    name: str = Field(...)


class ParcelTypes(BaseSchema):
    parcel_types: list[ParcelType] = Field(...)


class StatisticsOut(BaseSchema):
    date: str = Field(...)
    parcel_type: str = Field(..., gt=0)
    total_cost: float = Field(...)


class DailyStatisticsResponse(BaseSchema):
    data: list[StatisticsOut] = Field(...)


class CompanyAssigned(BaseSchema):
    parcel_id: str = Field(...)
    company_id: int = Field(...)


class CompanyAssignRequest(BaseSchema):
    company_id: int = Field(..., gt=0)
