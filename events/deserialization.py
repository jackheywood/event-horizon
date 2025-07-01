from datetime import datetime

from .base import Event
from .lights import LightSwitchedOn, LightSwitchedOff

EVENT_TYPE_MAP = {
    "LightSwitchedOn": LightSwitchedOn,
    "LightSwitchedOff": LightSwitchedOff,
}


def deserialize_event(data: dict) -> Event:
    data = data.copy()
    event_type = data.pop("type")
    cls = EVENT_TYPE_MAP.get(event_type)
    if not cls:
        raise ValueError(f"Unknown event type: {event_type}")
    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    return cls(**data)
