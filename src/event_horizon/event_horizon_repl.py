from cmd import Cmd

from event_horizon.aggregates import LightAggregate
from event_horizon.commands import NewLight, TurnOnLight, TurnOffLight
from event_horizon.domain import EventStore
from event_horizon.events import LightEvent
from event_horizon.handlers import LightHandler


class EventHorizonRepl(Cmd):
    intro = "\n🌌 Welcome to Event Horizon 🌌\n\nType help or ? to list commands."
    prompt = "\n>> "

    light_mapping = {
        "on": (TurnOnLight, "💡 Switched on"),
        "off": (TurnOffLight, "🔌 Switched off"),
        "create": (NewLight, "✅ Created"),
    }

    def __init__(self, handler: LightHandler, store: EventStore):
        super().__init__()
        self.handler = handler
        self.store = store

    def do_light(self, line):
        """Manage lights: light <on|off|create|show>"""
        parts = line.split()

        if not parts:
            print("Usage: light <on|off|create|show> <name> [is_on]")
            return

        cmd, *args = parts
        entry = self.light_mapping.get(cmd)

        if not entry:
            print("Unknown light command: ", cmd)
            return

        command_cls, msg = entry
        name = args[0] if args else None
        is_on = args[1].lower() == "true" if len(args) > 1 else None

        if not name:
            print(f"Usage: light {cmd} <name>")
            return

        is_create = cmd == "create"
        command = command_cls(name, is_on) if is_create else command_cls(name)

        try:
            self.handler.handle(command)
            suffix = " 💡" if is_on else (" 🔌" if is_create else "")
            print(f"{msg} {name}{suffix}")
        except Exception as e:
            print(f"❌ {e}")

    def do_lights(self, _):
        """ Show the current state of all lights: lights"""
        try:
            lights = self.store.load_all(LightAggregate, LightEvent)
            if not lights:
                print("No lights found. Try creating one with `light create <name>`.")
                return
            for light in lights:
                print(f"{light.aggregate_id}: {'💡 On' if light.is_on else '🔌 Off'}")
        except Exception as e:
            print(f"❌ {e}")

    def default(self, line):
        print(f"❓ Unknown command: {line}. Try `help`.")

    @staticmethod
    def do_exit(_):
        """Exit the application"""
        print("Thank you for using Event Horizon.")
        return True
