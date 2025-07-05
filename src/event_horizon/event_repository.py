import json
import os
from collections import defaultdict
from typing import Any, Generator


class EventRepository:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def save(self, event: dict[str, Any]) -> None:
        with open(self.file_name, "a") as file:
            file.write(json.dumps(event) + '\n')

    def load(
            self,
            category: str,
            aggregate_id: str,
    ) -> Generator[dict[str, Any], None, None]:
        if not os.path.exists(self.file_name):
            return
        with open(self.file_name, "r") as file:
            for line in file:
                event: dict = json.loads(line)
                if self._matches(event, category, aggregate_id):
                    yield event

    def load_all(self, category: str) -> dict[str, list[dict[str, Any]]]:
        if not os.path.exists(self.file_name):
            return {}
        aggregate_events = defaultdict(list)
        with open(self.file_name, "r") as file:
            for line in file:
                event: dict = json.loads(line)
                if event["category"] == category:
                    aggregate_events[event["aggregate_id"]].append(event)
        return aggregate_events

    @staticmethod
    def _matches(event: dict[str, Any], category: str, agg_id: str) -> bool:
        return (
                event["category"] == category
                and event["aggregate_id"] == agg_id
        )
