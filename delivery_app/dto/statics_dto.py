from dto.base_dto import BaseSchema


class StatisticsOut(BaseSchema):
    date: str
    parcel_type: str
    total_cost: float


class DailyStatisticsDTO(BaseSchema):
    data: list[StatisticsOut]
