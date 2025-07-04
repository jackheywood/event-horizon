from dataclasses import dataclass

from .base_event import Event


@dataclass(frozen=True)
class LightEvent(Event):
    pass


@dataclass(frozen=True)
class LightCreated(LightEvent):
    is_on: bool

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["is_on"] = self.is_on
        return data


@dataclass(frozen=True)
class LightSwitchedOn(LightEvent):
    pass


@dataclass(frozen=True)
class LightSwitchedOff(LightEvent):
    pass
