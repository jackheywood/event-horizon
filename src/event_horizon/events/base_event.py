from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event(ABC):
    timestamp: datetime
    aggregate_id: str

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        return {
            "category": self.category(),
            "type": self.type,
            "aggregate_id": self.aggregate_id,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    @abstractmethod
    def category(cls) -> str:
        """Returns the root event category (e.g. "LightEvent")"""
        ...
