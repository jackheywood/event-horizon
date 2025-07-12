from dataclasses import dataclass

from .base_command import Command


@dataclass(frozen=True)
class NewDoor(Command):
    is_open: bool = False


@dataclass(frozen=True)
class OpenDoor(Command):
    pass


@dataclass(frozen=True)
class CloseDoor(Command):
    pass
