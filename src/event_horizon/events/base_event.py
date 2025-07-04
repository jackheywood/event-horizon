from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    aggregate_id: str

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "aggregate_id": self.aggregate_id,
            "timestamp": self.timestamp.isoformat(),
        }
