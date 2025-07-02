from dataclasses import dataclass

from .base_command import Command


@dataclass(frozen=True)
class NewLight(Command):
    is_on: bool = False


@dataclass(frozen=True)
class TurnOnLight(Command):
    pass


@dataclass(frozen=True)
class TurnOffLight(Command):
    pass
