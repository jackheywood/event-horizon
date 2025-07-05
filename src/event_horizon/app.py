from event_horizon.event_horizon_repl import EventHorizonRepl
from event_horizon.event_repository import EventRepository
from event_horizon.event_store import EventStore
from event_horizon.handlers import LightHandler


def main():
    event_repository = EventRepository("event_log.jsonl")
    event_store = EventStore(event_repository)
    light_handler = LightHandler(event_store)
    repl = EventHorizonRepl(light_handler, event_store)
    repl.cmdloop()
