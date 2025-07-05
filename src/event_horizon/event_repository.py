import json
from typing import Generator


class EventRepository:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def save(self, event: dict):
        with open(self.file_name, "a") as file:
            file.write(json.dumps(event) + '\n')

    def load(self, category: str, aggregate_id: str) -> Generator[dict, None, None]:
        with open(self.file_name, "r") as file:
            for line in file:
                event: dict = json.loads(line)
                if event["category"] == category and event["aggregate_id"] == aggregate_id:
                    yield event
