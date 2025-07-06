from datetime import datetime
from unittest.mock import MagicMock, call

import pytest

from event_horizon.aggregates import LightAggregate
from event_horizon.domain import EventStore
from event_horizon.events import LightCreated, LightSwitchedOn, LightEvent


@pytest.fixture
def event_data():
    return {
        "kitchen_events": [
            {
                "category": "LightEvent",
                "type": "LightCreated",
                "aggregate_id": "kitchen",
                "timestamp": datetime.now().isoformat(),
                "is_on": False,
            },
            {
                "category": "LightEvent",
                "type": "LightSwitchedOn",
                "aggregate_id": "kitchen",
                "timestamp": datetime.now().isoformat(),
            },
        ],
        "bedroom_events": [
            {
                "category": "LightEvent",
                "type": "LightCreated",
                "aggregate_id": "bedroom",
                "timestamp": datetime.now().isoformat(),
                "is_on": True,
            },
            {
                "category": "LightEvent",
                "type": "LightSwitchedOff",
                "aggregate_id": "kitchen",
                "timestamp": datetime.now().isoformat(),
            }
        ]
    }


def test_save_saves_uncommitted_events():
    # Arrange
    events = [
        LightCreated(datetime.now(), "kitchen", False),
        LightSwitchedOn(datetime.now(), "kitchen"),
    ]

    mock_repo = MagicMock()
    mock_aggregate = MagicMock()
    mock_aggregate.get_uncommitted_events.return_value = events

    store = EventStore(mock_repo)

    # Act
    store.save(mock_aggregate)

    # Assert
    assert mock_repo.save.call_count == 2

    mock_repo.save.assert_has_calls([
        call({
            "category": "LightEvent",
            "type": "LightCreated",
            "aggregate_id": "kitchen",
            "timestamp": events[0].timestamp.isoformat(),
            "is_on": False,
        }),
        call({
            "category": "LightEvent",
            "type": "LightSwitchedOn",
            "aggregate_id": "kitchen",
            "timestamp": events[1].timestamp.isoformat(),
        }),
    ])


def test_save_clears_uncommitted_events():
    # Arrange
    mock_aggregate = MagicMock()
    store = EventStore(MagicMock())

    # Act
    store.save(mock_aggregate)

    # Assert
    mock_aggregate.clear_uncommitted_events.assert_called_once()


def test_load_all_returns_rehydrated_aggregates(event_data):
    # Arrange
    mock_repo = MagicMock()
    mock_repo.load_all.return_value = {
        "kitchen": event_data["kitchen_events"],
        "bedroom": event_data["bedroom_events"],
    }

    store = EventStore(mock_repo)

    # Act
    aggregates = store.load_all(LightAggregate, LightEvent)

    # Assert
    assert len(aggregates) == 2

    assert aggregates[0].aggregate_id == "bedroom"
    assert aggregates[0].is_on is False

    assert aggregates[1].aggregate_id == "kitchen"
    assert aggregates[1].is_on is True

    mock_repo.load_all.assert_called_once_with("LightEvent")


def test_load_returns_rehydrated_aggregate(event_data):
    # Arrange
    mock_repo = MagicMock()
    mock_repo.load.return_value = event_data["bedroom_events"]

    store = EventStore(mock_repo)

    # Act
    aggregate = store.load(LightAggregate, LightEvent, "bedroom")

    # Assert
    assert aggregate.aggregate_id == "bedroom"
    assert aggregate.is_on is False

    mock_repo.load.assert_called_once_with("LightEvent", "bedroom")


def test_load_raises_exception_for_nonexistent_aggregate_id():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.load.return_value = []

    store = EventStore(mock_repo)

    # Act
    with pytest.raises(ValueError) as error:
        store.load(LightAggregate, LightEvent, "bedroom")

    # Assert
    assert str(error.value) == (
        "No events found for LightAggregate "
        "with id bedroom"
    )

    mock_repo.load.assert_called_once_with("LightEvent", "bedroom")


def test_exists_returns_false_when_no_events_found():
    # Arrange
    mock_repo = MagicMock()
    mock_repo.load.return_value = []

    store = EventStore(mock_repo)

    # Act
    result = store.exists(LightEvent, "kitchen")

    # Assert
    assert result is False
    mock_repo.load.assert_called_once_with("LightEvent", "kitchen")


def test_exists_returns_true_when_events_found(event_data):
    # Arrange
    mock_repo = MagicMock()
    mock_repo.load.return_value = event_data["kitchen_events"]

    store = EventStore(mock_repo)

    # Act
    result = store.exists(LightEvent, "kitchen")

    # Assert
    assert result is True
    mock_repo.load.assert_called_once_with("LightEvent", "kitchen")
