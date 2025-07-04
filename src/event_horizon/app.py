from event_horizon.aggregates import LightAggregate
from event_horizon.commands import NewLight, TurnOnLight, TurnOffLight
from event_horizon.event_store import EventStore
from event_horizon.events import LightEvent
from event_horizon.handlers import LightHandler


def main():
    event_store = EventStore()
    light_handler = LightHandler(event_store)
    light_id = "kitchen"

    light_handler.handle(NewLight(light_id))
    light_handler.handle(TurnOnLight(light_id))
    light_handler.handle(TurnOffLight(light_id))

    aggregate = event_store.load(LightAggregate, LightEvent, light_id)
    print(aggregate)
