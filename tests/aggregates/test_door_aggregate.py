from datetime import datetime

import pytest
from freezegun import freeze_time

from event_horizon.aggregates import DoorAggregate
from event_horizon.events import DoorCreated, DoorClosed, DoorOpened


@pytest.fixture
def aggregate_id():
    return "garden"


@pytest.mark.parametrize("is_open", [True, False])
def test_create_creates_door_aggregate(aggregate_id: str, is_open: bool):
    # Act
    aggregate = DoorAggregate.create(aggregate_id, is_open)

    # Assert
    assert aggregate.aggregate_id == aggregate_id
    assert aggregate.is_open is is_open
    assert aggregate._was_created is True


@freeze_time("2025-07-12")
@pytest.mark.parametrize("is_open", [True, False])
def test_create_raises_created_event(aggregate_id: str, is_open: bool):
    # Act
    aggregate = DoorAggregate.create(aggregate_id, is_open)
    events = aggregate._changes

    # Assert
    assert len(events) == 1
    event = events[0]

    assert isinstance(event, DoorCreated)
    assert event.aggregate_id == aggregate_id
    assert event.is_open is is_open
    assert event.timestamp == datetime(2025, 7, 12)


def test_create_already_created_raises_exception(aggregate_id):
    # Act
    aggregate = DoorAggregate.create(aggregate_id)

    # Act
    with pytest.raises(Exception) as error:
        aggregate._raise_event(
            DoorCreated(datetime.now(), aggregate_id, False),
        )

    # Assert
    assert str(error.value) == "Door has already been created"


def test_rehydrate_plays_events(aggregate_id):
    # Arrange
    events = [
        DoorCreated(datetime.now(), aggregate_id, True),
        DoorClosed(datetime.now(), aggregate_id),
    ]

    # Act
    aggregate = DoorAggregate.rehydrate(aggregate_id, events)

    # Assert
    assert aggregate.is_open is False
    assert aggregate.aggregate_id == aggregate_id
    assert aggregate.get_uncommitted_events() == []


def test_open_opens_door(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id)

    # Act
    aggregate.open()

    # Assert
    assert aggregate.is_open is True


@freeze_time("2023-12-03")
def test_open_raises_opened_event(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id)

    # Act
    aggregate.open()
    events = aggregate._changes

    # Assert
    assert len(events) == 2
    event = events[1]

    assert isinstance(event, DoorOpened)
    assert event.aggregate_id == aggregate_id
    assert event.timestamp == datetime(2023, 12, 3)


def test_open_already_open_raises_exception(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id, True)

    # Act
    with pytest.raises(Exception) as error:
        aggregate.open()

    # Assert
    assert str(error.value) == "Door is already open"


def test_close_closes_door(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id, True)

    # Act
    aggregate.close()

    # Assert
    assert aggregate.is_open is False


@freeze_time("2025-04-28")
def test_close_raises_closed_event(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id, True)

    # Act
    aggregate.close()
    events = aggregate._changes

    # Assert
    assert len(events) == 2
    event = events[1]

    assert isinstance(event, DoorClosed)
    assert event.aggregate_id == aggregate_id
    assert event.timestamp == datetime(2025, 4, 28)


def test_close_already_closed_raises_exception(aggregate_id):
    # Arrange
    aggregate = DoorAggregate.create(aggregate_id, False)

    # Act
    with pytest.raises(Exception) as error:
        aggregate.close()

    # Assert
    assert str(error.value) == "Door is already closed"


def test_get_uncommitted_events_returns_changes(aggregate_id):
    # Arrange
    changes = [
        DoorCreated(datetime.now(), aggregate_id, True),
        DoorClosed(datetime.now(), aggregate_id),
        DoorOpened(datetime.now(), aggregate_id),
    ]
    aggregate = DoorAggregate(aggregate_id)
    aggregate._changes = changes

    # Act
    events = aggregate.get_uncommitted_events()

    # Assert
    assert events == changes


def test_clear_uncommitted_events_clears_changes(aggregate_id):
    # Arrange
    aggregate = DoorAggregate(aggregate_id)
    aggregate._changes = [
        DoorCreated(datetime.now(), aggregate_id, True),
        DoorClosed(datetime.now(), aggregate_id),
    ]

    # Act
    aggregate.clear_uncommitted_events()

    # Assert
    assert aggregate._changes == []


def test_light_lifecycle_end_to_end(aggregate_id):
    # Create and open a door
    aggregate = DoorAggregate.create(aggregate_id)
    aggregate.open()

    # Capture events
    events = aggregate.get_uncommitted_events()
    aggregate.clear_uncommitted_events()

    # Rehydrate from events
    new_aggregate = DoorAggregate.rehydrate(aggregate_id, events)

    # Assert final state
    assert new_aggregate.is_open is True
    assert new_aggregate.aggregate_id == aggregate_id
    assert new_aggregate.get_uncommitted_events() == []
    assert new_aggregate._was_created is True
