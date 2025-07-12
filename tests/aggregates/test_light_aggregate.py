from datetime import datetime

import pytest
from freezegun import freeze_time

from event_horizon.aggregates import LightAggregate
from event_horizon.events import LightCreated, LightSwitchedOff, LightSwitchedOn


@pytest.fixture
def aggregate_id():
    return "bathroom"


@pytest.mark.parametrize("is_on", [True, False])
def test_create_creates_light_aggregate(aggregate_id: str, is_on: bool):
    # Act
    aggregate = LightAggregate.create(aggregate_id, is_on)

    # Assert
    assert aggregate.aggregate_id == aggregate_id
    assert aggregate.is_on is is_on
    assert aggregate._was_created is True


@freeze_time("2025-07-01T17:20:40")
@pytest.mark.parametrize("is_on", [True, False])
def test_create_raises_created_event(aggregate_id: str, is_on: bool):
    # Act
    aggregate = LightAggregate.create(aggregate_id, is_on)
    events = aggregate._changes

    # Assert
    assert len(events) == 1
    event = events[0]

    assert isinstance(event, LightCreated)
    assert event.aggregate_id == aggregate_id
    assert event.is_on is is_on
    assert event.timestamp == datetime(2025, 7, 1, 17, 20, 40)


def test_create_already_created_raises_exception(aggregate_id):
    # Act
    aggregate = LightAggregate.create(aggregate_id)

    # Act
    with pytest.raises(Exception) as error:
        aggregate._raise_event(
            LightCreated(datetime.now(), aggregate_id, False),
        )

    # Assert
    assert str(error.value) == "Light already created"


def test_rehydrate_plays_events(aggregate_id):
    # Arrange
    events = [
        LightCreated(datetime.now(), aggregate_id, True),
        LightSwitchedOff(datetime.now(), aggregate_id),
    ]

    # Act
    aggregate = LightAggregate.rehydrate(aggregate_id, events)

    # Assert
    assert aggregate.is_on is False
    assert aggregate.aggregate_id == aggregate_id
    assert aggregate.get_uncommitted_events() == []


def test_turn_on_turns_on_light(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id)

    # Act
    aggregate.turn_on()

    # Assert
    assert aggregate.is_on is True


@freeze_time("2021-12-03")
def test_turn_on_raises_switched_on_event(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id)

    # Act
    aggregate.turn_on()
    events = aggregate._changes

    # Assert
    assert len(events) == 2
    event = events[1]

    assert isinstance(event, LightSwitchedOn)
    assert event.aggregate_id == aggregate_id
    assert event.timestamp == datetime(2021, 12, 3)


def test_turn_on_already_on_raises_exception(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id, True)

    # Act
    with pytest.raises(Exception) as error:
        aggregate.turn_on()

    # Assert
    assert str(error.value) == "Light is already switched on"


def test_turn_off_turns_off_light(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id, True)

    # Act
    aggregate.turn_off()

    # Assert
    assert aggregate.is_on is False


@freeze_time("2022-04-28")
def test_turn_off_raises_switched_off_event(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id, True)

    # Act
    aggregate.turn_off()
    events = aggregate._changes

    # Assert
    assert len(events) == 2
    event = events[1]

    assert isinstance(event, LightSwitchedOff)
    assert event.aggregate_id == aggregate_id
    assert event.timestamp == datetime(2022, 4, 28)


def test_turn_off_already_off_raises_exception(aggregate_id):
    # Arrange
    aggregate = LightAggregate.create(aggregate_id, False)

    # Act
    with pytest.raises(Exception) as error:
        aggregate.turn_off()

    # Assert
    assert str(error.value) == "Light is already switched off"


def test_get_uncommitted_events_returns_changes(aggregate_id):
    # Arrange
    changes = [
        LightCreated(datetime.now(), aggregate_id, True),
        LightSwitchedOff(datetime.now(), aggregate_id),
        LightSwitchedOn(datetime.now(), aggregate_id),
    ]
    aggregate = LightAggregate(aggregate_id)
    aggregate._changes = changes

    # Act
    events = aggregate.get_uncommitted_events()

    # Assert
    assert events == changes


def test_clear_uncommitted_events_clears_changes(aggregate_id):
    # Arrange
    aggregate = LightAggregate(aggregate_id)
    aggregate._changes = [
        LightCreated(datetime.now(), aggregate_id, True),
        LightSwitchedOff(datetime.now(), aggregate_id),
    ]

    # Act
    aggregate.clear_uncommitted_events()

    # Assert
    assert aggregate._changes == []


def test_light_lifecycle_end_to_end(aggregate_id):
    # Create and turn light on
    aggregate = LightAggregate.create(aggregate_id, False)
    aggregate.turn_on()

    # Capture events
    events = aggregate.get_uncommitted_events()
    aggregate.clear_uncommitted_events()

    # Rehydrate from events
    new_aggregate = LightAggregate.rehydrate(aggregate_id, events)

    # Assert final state
    assert new_aggregate.is_on is True
    assert new_aggregate.aggregate_id == aggregate_id
    assert new_aggregate.get_uncommitted_events() == []
    assert new_aggregate._was_created is True
