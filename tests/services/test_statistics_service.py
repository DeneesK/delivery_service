import pytest
from datetime import datetime

from delivery_app.dto.statics_dto import DailyStatisticsDTO
from delivery_app.services.statistics import StatisticsService


@pytest.mark.asyncio
async def test_get_daily_costs_with_parcel_type(
    statistics_service: StatisticsService, mock_mongo_collection
):
    # Arrange
    mock_result = [
        {
            "parcel_type": "clothes",
            "total_cost": 100.0,
            "date": "2025-07-06",
        }
    ]
    mock_mongo_collection.aggregate.return_value.to_list.return_value = mock_result

    # Act
    date = datetime(2025, 7, 6)
    result: DailyStatisticsDTO = await statistics_service.get_daily_costs(
        date, parcel_type="clothes"
    )

    # Assert
    assert result.data[0].parcel_type == "clothes"
    assert result.data[0].total_cost == 100.0
    assert result.data[0].date == "2025-07-06"


@pytest.mark.asyncio
async def test_get_daily_costs_without_parcel_type(
    statistics_service: StatisticsService, mock_mongo_collection
):
    # Arrange
    mock_result = [
        {
            "parcel_type": "electronics",
            "total_cost": 150.0,
            "date": "2025-07-06",
        }
    ]
    mock_mongo_collection.aggregate.return_value.to_list.return_value = mock_result

    # Act
    date = datetime(2025, 7, 6)
    result: DailyStatisticsDTO = await statistics_service.get_daily_costs(date)

    # Assert
    assert result.data[0].parcel_type == "electronics"
    assert result.data[0].total_cost == 150.0
    assert result.data[0].date == "2025-07-06"
