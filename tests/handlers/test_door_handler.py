from typing import Callable
from unittest.mock import MagicMock, patch

import pytest

from event_horizon.aggregates import DoorAggregate
from event_horizon.commands import Command, NewDoor, OpenDoor, CloseDoor
from event_horizon.events import DoorEvent
from event_horizon.handlers import DoorHandler


@pytest.fixture
def aggregate_id():
    return "shed"


@pytest.mark.parametrize("command_cls,called,not_called", [
    (OpenDoor, "open", "close"),
    (CloseDoor, "close", "open"),
])
def test_handles_opens_or_close_door_commands(
        aggregate_id: str,
        command_cls: Callable[[str], Command],
        called: str,
        not_called: str,
):
    # Arrange
    mock_store = MagicMock()
    mock_aggregate = MagicMock()
    mock_store.load.return_value = mock_aggregate

    with (patch.object(DoorAggregate, "create") as mock_create):
        handler = DoorHandler(mock_store)
        command = command_cls(aggregate_id)

        # Act
        handler.handle(command)

        # Assert
        mock_store.load.assert_called_once_with(
            DoorAggregate,
            DoorEvent,
            aggregate_id
        )
        mock_store.save.assert_called_once_with(mock_aggregate)

        getattr(mock_aggregate, called).assert_called_once()
        getattr(mock_aggregate, not_called).assert_not_called()

        mock_create.assert_not_called()


def test_handles_new_door_command(aggregate_id):
    # Arrange
    mock_store = MagicMock()
    mock_aggregate = MagicMock()
    mock_store.exists.return_value = False

    with (patch.object(
            DoorAggregate,
            "create",
            return_value=mock_aggregate)
    as mock_create):
        handler = DoorHandler(mock_store)
        command = NewDoor(aggregate_id, True)

        # Act
        handler.handle(command)

        # Assert
        mock_create.assert_called_once_with(aggregate_id, True)

        mock_store.save.assert_called_once_with(mock_aggregate)
        mock_store.load.assert_not_called()

        mock_aggregate.open.assert_not_called()
        mock_aggregate.close.assert_not_called()


def test_raises_exception_for_existing_new_door(aggregate_id):
    # Arrange
    mock_store = MagicMock()
    mock_aggregate = MagicMock()
    mock_store.exists.return_value = True

    with (patch.object(DoorAggregate, "create") as mock_create):
        handler = DoorHandler(mock_store)
        command = NewDoor(aggregate_id, True)

        # Act
        with pytest.raises(Exception) as error:
            handler.handle(command)

        # Assert
        assert str(error.value) == f"Door with id '{aggregate_id}' already exists"

        mock_create.assert_not_called()

        mock_store.save.assert_not_called()
        mock_store.load.assert_not_called()

        mock_aggregate.open.assert_not_called()
        mock_aggregate.close.assert_not_called()
