from datetime import datetime

import pytest

from event_horizon.events import deserialize_event
from event_horizon.events.lights import LightSwitchedOn, LightSwitchedOff


@pytest.fixture
def event_data():
    return {
        "event_id": "kitchen",
        "timestamp_string": "2025-07-01T17:20:40",
        "timestamp": datetime.fromisoformat("2025-07-01T17:20:40"),
    }


@pytest.mark.parametrize("event_type,expected_class", [
    ("LightSwitchedOff", LightSwitchedOff),
    ("LightSwitchedOn", LightSwitchedOn),
])
def test_deserialize_light_event(event_data, event_type, expected_class):
    # Arrange
    data = {
        "type": event_type,
        "light_id": event_data["event_id"],
        "timestamp": event_data["timestamp_string"],
    }

    # Act
    event = deserialize_event(data)

    # Assert
    assert isinstance(event, expected_class)
    assert event.light_id == event_data["event_id"]
    assert event.timestamp == event_data["timestamp"]
