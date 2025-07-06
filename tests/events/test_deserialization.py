from datetime import datetime

import pytest

from event_horizon.events import deserialize_event
from event_horizon.events.light_events import LightCreated, LightSwitchedOn, LightSwitchedOff


@pytest.fixture
def timestamp():
    return datetime.fromisoformat("2025-07-01T17:20:40")


@pytest.fixture
def event_data(timestamp):
    return {
        "aggregate_id": "kitchen",
        "category": "LightEvent",
        "timestamp": timestamp,
        "timestamp_string": timestamp.isoformat(),
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
        "category": event_data["category"],
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


def test_deserialize_unknown_event_type_raises():
    # Arrange
    data = {"type": "InvalidEvent"}

    # Act
    with pytest.raises(ValueError) as error:
        deserialize_event(data)

    # Assert
    assert str(error.value) == "Unknown event type: InvalidEvent"


def test_deserialize_wrong_args_raises(event_data):
    # Arrange
    data = {
        "category": event_data["category"],
        "type": "LightCreated",
        "light_id": "kitchen",
        "timestamp": event_data["timestamp_string"],
    }

    # Act
    with pytest.raises(ValueError) as error:
        deserialize_event(data)

    # Assert
    assert "unexpected keyword argument 'light_id'" in str(error.value)
