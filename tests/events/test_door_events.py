from datetime import datetime
from typing import Callable

import pytest

from event_horizon.events import Event, DoorCreated, DoorOpened, DoorClosed


@pytest.fixture
def timestamp():
    return datetime.fromisoformat("2025-07-01T17:20:40")


@pytest.mark.parametrize("event_cls,kwargs,expected_dict", [
    (
            DoorCreated,
            {"is_open": True},
            {"type": "DoorCreated", "is_open": True}
    ),
    (
            DoorOpened,
            {},
            {"type": "DoorOpened"}
    ),
    (
            DoorClosed,
            {},
            {"type": "DoorClosed"}
    ),
])
def test_door_events_to_dict(
        timestamp: datetime,
        event_cls: Callable[..., Event],
        kwargs: dict,
        expected_dict: dict,
):
    # Arrange
    aggregate_id = "front"
    event = event_cls(timestamp, aggregate_id, **kwargs)

    # Act
    result = event.to_dict()

    # Assert
    assert result == {
        **expected_dict,
        "category": "DoorEvent",
        "aggregate_id": aggregate_id,
        "timestamp": timestamp.isoformat(),
    }
