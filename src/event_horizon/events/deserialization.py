from datetime import datetime

from .base_event import Event
from .door_events import DoorCreated, DoorOpened, DoorClosed
from .light_events import LightCreated, LightSwitchedOn, LightSwitchedOff

EVENT_TYPE_MAP: dict[str, type[Event]] = {
    "LightCreated": LightCreated,
    "LightSwitchedOn": LightSwitchedOn,
    "LightSwitchedOff": LightSwitchedOff,
    "DoorCreated": DoorCreated,
    "DoorOpened": DoorOpened,
    "DoorClosed": DoorClosed,
}


def deserialize_event(data: dict) -> Event:
    data = data.copy()
    event_type = data.pop("type")
    cls = EVENT_TYPE_MAP.get(event_type)

    if not cls:
        raise ValueError(f"Unknown event type: {event_type}")

    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    data.pop("category")  # Not needed

    try:
        return cls(**data)  # type: ignore
    except TypeError as e:
        raise ValueError(f"Invalid event data: {e}")
