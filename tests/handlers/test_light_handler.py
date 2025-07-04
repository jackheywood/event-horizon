from typing import Callable
from unittest.mock import MagicMock, patch

import pytest

from event_horizon.aggregates import LightAggregate
from event_horizon.commands import Command, TurnOnLight, TurnOffLight, NewLight
from event_horizon.events import LightEvent
from event_horizon.handlers import LightHandler


@pytest.mark.parametrize("command_cls,called,not_called", [
    (TurnOnLight, "turn_on", "turn_off"),
    (TurnOffLight, "turn_off", "turn_on"),
])
def test_handles_turn_on_or_off_light(
        command_cls: Callable[[str], Command],
        called: str,
        not_called: str,
):
    # Arrange
    mock_store = MagicMock()
    mock_aggregate = MagicMock()
    mock_store.load.return_value = mock_aggregate

    with (patch.object(LightAggregate, "create") as mock_create):
        handler = LightHandler(mock_store)
        command = command_cls("kitchen")

        # Act
        handler.handle(command)

        # Assert
        mock_store.load.assert_called_once_with(
            LightAggregate,
            LightEvent,
            "kitchen"
        )
        mock_store.save.assert_called_once_with(mock_aggregate)

        getattr(mock_aggregate, called).assert_called_once()
        getattr(mock_aggregate, not_called).assert_not_called()

        mock_create.assert_not_called()


def test_handles_new_light_command():
    # Arrange
    mock_store = MagicMock()
    mock_aggregate = MagicMock()

    with (patch.object(
            LightAggregate,
            "create",
            return_value=mock_aggregate)
    as mock_create):
        handler = LightHandler(mock_store)
        command = NewLight("kitchen", True)

        # Act
        handler.handle(command)

        # Assert
        mock_create.assert_called_once_with("kitchen", True)

        mock_store.save.assert_called_once_with(mock_aggregate)
        mock_store.load.assert_not_called()

        mock_aggregate.turn_on.assert_not_called()
        mock_aggregate.turn_off.assert_not_called()
