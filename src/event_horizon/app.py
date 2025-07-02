from event_horizon.commands.light_commands import NewLight, TurnOnLight, TurnOffLight
from event_horizon.event_store import get_aggregate
from event_horizon.handlers.light_handler import handle_light_command


def main():
    light_id = "kitchen"
    handle_light_command(NewLight(light_id))
    handle_light_command(TurnOnLight(light_id))
    handle_light_command(TurnOffLight(light_id))
    aggregate = get_aggregate(light_id)
    print(aggregate)
