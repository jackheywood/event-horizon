from datetime import datetime

from .base import Event


class LightEvent(Event):
    def __init__(self, light_id: str, timestamp: datetime):
        super().__init__(timestamp)
        self.light_id = light_id

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["light_id"] = self.light_id
        return data


class LightSwitchedOn(LightEvent):
    def __init__(self, light_id: str, timestamp: datetime):
        super().__init__(light_id, timestamp)


class LightSwitchedOff(LightEvent):
    def __init__(self, light_id: str, timestamp: datetime):
        super().__init__(light_id, timestamp)
