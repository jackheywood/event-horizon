from datetime import datetime
from typing import Callable

import pytest

from event_horizon.events import Event, LightCreated, LightSwitchedOn, LightSwitchedOff


@pytest.fixture
def timestamp():
    return datetime.fromisoformat("2025-07-01T17:20:40")


@pytest.mark.parametrize("event_cls,kwargs,expected_dict", [
    (
            LightCreated,
            {"is_on": True},
            {"type": "LightCreated", "is_on": True}
    ),
    (
            LightSwitchedOn,
            {},
            {"type": "LightSwitchedOn"}
    ),
    (
            LightSwitchedOff,
            {},
            {"type": "LightSwitchedOff"}
    ),
])
def test_light_events_to_dict(
        timestamp: datetime,
        event_cls: Callable[..., Event],
        kwargs: dict,
        expected_dict: dict,
):
    # Arrange
    aggregate_id = "kitchen"
    event = event_cls(timestamp, aggregate_id, **kwargs)

    # Act
    result = event.to_dict()

    # Assert
    assert result == {
        **expected_dict,
        "aggregate_id": aggregate_id,
        "timestamp": timestamp.isoformat(),
    }
