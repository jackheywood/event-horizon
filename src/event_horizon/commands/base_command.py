from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    aggregate_id: str
