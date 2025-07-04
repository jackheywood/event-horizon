from datetime import datetime

import pytest

from event_horizon.events import deserialize_event
from event_horizon.events.light_events import LightCreated, LightSwitchedOn, LightSwitchedOff


@pytest.fixture
def event_data():
    return {
        "aggregate_id": "kitchen",
        "timestamp_string": "2025-07-01T17:20:40",
        "timestamp": datetime.fromisoformat("2025-07-01T17:20:40"),
        "is_on": True
    }


@pytest.mark.parametrize("event_type,expected_class,is_created", [
    ("LightCreated", LightCreated, True),
    ("LightSwitchedOff", LightSwitchedOff, False),
    ("LightSwitchedOn", LightSwitchedOn, False),
])
def test_deserialize_light_event(event_data, event_type, expected_class, is_created):
    # Arrange
    data = {
        "type": event_type,
        "aggregate_id": event_data["aggregate_id"],
        "timestamp": event_data["timestamp_string"],
    }

    if is_created:
        data["is_on"] = event_data["is_on"]

    # Act
    event = deserialize_event(data)

    # Assert
    assert isinstance(event, expected_class)
    assert event.aggregate_id == event_data["aggregate_id"]
    assert event.timestamp == event_data["timestamp"]
    if is_created:
        assert event.is_on == event_data["is_on"]
