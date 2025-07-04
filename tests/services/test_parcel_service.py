import pytest

from delivery_app.services.parcel import ParcelService


@pytest.mark.asyncio
async def test_mock_new_parcel_success(mock_task_client, mock_session):
    service = ParcelService(session_maker=mock_session, task_client=mock_task_client)

    parcel_id = await service.new_parcel("Parcel1", 1.0, "clothes", 100.0, "user1")

    assert isinstance(parcel_id, str)
    assert len(parcel_id) > 0

    mock_task_client.send_task.assert_called_once()
    called_args = mock_task_client.send_task.call_args.args
    assert called_args[0] == "consumer.tasks.register_parcel_task"

    parcel_data_arg = called_args[1][0]
    assert parcel_data_arg["name"] == "Parcel1"
    assert parcel_data_arg["weight"] == 1.0
    assert parcel_data_arg["parcel_type"] == "clothes"
    assert parcel_data_arg["content_value_usd"] == 100.0
    assert parcel_data_arg["owner"] == "user1"
    assert parcel_data_arg["parcel_id"] == parcel_id


@pytest.mark.asyncio
async def test_mock_get_parcel_by_id_success(mock_parcel_service):
    parcel_id = "1234"
    result = await mock_parcel_service.get_by_id(parcel_id)

    assert result.parcel_id == parcel_id


@pytest.mark.asyncio
async def test_mock_get_parcel_by_owner_success(mock_parcel_service):
    owner = "user"
    result = await mock_parcel_service.get_all_parcels(
        owner=owner, parcel_type="clothes", has_delivery_cost=True
    )

    assert isinstance(result, list)
