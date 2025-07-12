from event_horizon.domain import EventStore
from event_horizon.event_horizon_repl import EventHorizonRepl
from event_horizon.handlers import LightHandler, DoorHandler
from event_horizon.persistence import EventRepository


def main():
    event_repository = EventRepository("event_log.jsonl")
    event_store = EventStore(event_repository)
    light_handler = LightHandler(event_store)
    door_handler = DoorHandler(event_store)
    repl = EventHorizonRepl(light_handler, door_handler, event_store)
    repl.cmdloop()
