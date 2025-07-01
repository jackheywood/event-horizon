from datetime import datetime


class Event:
    def __init__(self, timestamp: datetime):
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "timestamp": self.timestamp.isoformat(),
        }

    def __repr__(self):
        return str(self.to_dict())
