from datetime import datetime

import pytest

from event_horizon.events import LightCreated, LightSwitchedOn, LightSwitchedOff


@pytest.fixture
def event_data():
    return {
        "aggregate_id": "kitchen",
        "timestamp_string": "2025-07-01T17:20:40",
        "timestamp": datetime.fromisoformat("2025-07-01T17:20:40"),
    }


def test_light_created_event_to_dict(event_data):
    # Arrange
    created_event = LightCreated(event_data["timestamp"], event_data["aggregate_id"], True)

    # Act
    event_dict = created_event.to_dict()

    # Assert
    assert event_dict == {
        "type": "LightCreated",
        "aggregate_id": event_data["aggregate_id"],
        "timestamp": event_data["timestamp_string"],
        "is_on": True,
    }


def test_light_switched_on_event_to_dict(event_data):
    # Arrange
    on_event = LightSwitchedOn(event_data["timestamp"], event_data["aggregate_id"])

    # Act
    event_dict = on_event.to_dict()

    # Assert
    assert event_dict == {
        "type": "LightSwitchedOn",
        "aggregate_id": event_data["aggregate_id"],
        "timestamp": event_data["timestamp_string"],
    }


def test_light_switched_off_event_to_dict(event_data):
    # Arrange
    off_event = LightSwitchedOff(event_data["timestamp"], event_data["aggregate_id"])

    # Act
    event_dict = off_event.to_dict()

    # Assert
    assert event_dict == {
        "type": "LightSwitchedOff",
        "aggregate_id": event_data["aggregate_id"],
        "timestamp": event_data["timestamp_string"],
    }
