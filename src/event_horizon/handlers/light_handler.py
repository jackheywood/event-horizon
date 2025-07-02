from event_horizon.aggregates import LightAggregate
from event_horizon.commands import Command, NewLight, TurnOnLight, TurnOffLight
from event_horizon.event_store import get_aggregate, save_aggregate


def handle_light_command(command: Command):
    if isinstance(command, NewLight):
        aggregate = LightAggregate(command.aggregate_id, command.is_on)
        save_aggregate(aggregate)

    elif isinstance(command, TurnOnLight):
        aggregate = get_aggregate(command.aggregate_id)
        aggregate.turn_on()

    elif isinstance(command, TurnOffLight):
        aggregate = get_aggregate(command.aggregate_id)
        aggregate.turn_off()

    else:
        raise Exception(f"Unknown command {command.__class__.__name__}")
