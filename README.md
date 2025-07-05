# 🌌 Event Horizon

> ⚠️ **Note:** This project is in early development. Most functionality is still
> being implemented, but the foundation is in place.

**Event Horizon** is a DIY, event-sourced home automation system built from
scratch in Python with no third-party libraries.

It’s a learning project, a tinkerer’s sandbox, and the seed of a long-term plan
to automate your home from the comfort of a clean, append-only event log.
All state is derived from a sequence of domain events.

No shortcuts. No YAML hell. Just Python.

## 🚀 Vision

- Build a minimal **event-sourcing engine** in pure Python
- Represent all system changes as discrete, timestamped **events**
- Rebuild **current state** on startup by replaying those events
- Control the system via a **CLI REPL**
- Evolve into a Pi-powered **home automation brain**

## 🛠️ Core Features (MVP)

- [ ] Define event types (e.g. `LightSwitchedOn`, `LightSwitchedOff`)
- [ ] Implement a file-based, append-only event store
- [ ] Rebuild the in-memory state by replaying events
- [ ] Handle commands like "turn light on/off"
- [ ] Interactive CLI for controlling and inspecting the system

## 📁 Project Structure (WIP)

```text
event-horizon/
├── src/
│   └── event_horizon/
│       ├── aggregates/            # Domain aggregates (state + behavior)
│       ├── commands/              # Command data structures
│       ├── events/                # Event definitions and deserialization logic
│       ├── handlers/              # Command handlers (map intent to aggregates)
│       ├── __init__.py            # Package marker
│       ├── app.py                 # CLI entrypoint
│       ├── event_repository.py    # Low-level event persistence
│       └── event_store.py         # Aggregate loading/saving via events
├── tests/                         # Unit tests
├── run.py                         # Script entrypoint for running the app
├── pyproject.toml                 # Build and dependency configuration (Poetry)
├── event_log.jsonl                # Append-only persistent event log (ignored in Git)
└── README.md
```

## 🧠 Future Directions

Once the MVP is in place, future expansions might include:

- 🧲 **GPIO input/output** via Raspberry Pi for real-world control
- 🌐 **REST API** for remote toggling or state inspection
- 📋 **Web dashboard** for live monitoring
- 🕒 **Time-based automations** (e.g. "turn lights on at sunset")
- 🌀 **Snapshots & time travel** tools for debugging or rollback
- 🤖 **Rule engine** for complex logic (e.g. motion + time = lights)

## 🧰 Getting Started

### 📦 Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation) installed

### 💻 Cloning and Running

Clone the repository:

```bash
git clone https://github.com/jackheywood/event-horizon.git
cd event-horizon
```

Install dependencies and set up the virtual environment:

```bash
poetry install
```

Run the app:

```bash
poetry run python run.py
```

You'll be dropped into a CLI where you can issue commands like:

```text
>>> on kitchen
>>> off hallway
>>> status
```

> ⚠️ **Note:** These commands are not implemented yet.

### 🧪 Running Tests

To run the unit tests:

```bash
poetry run pytest
```

## ⏳ Status

Currently in early development.  
Jack is building this system one event at a time.

## 📜 License

Unlicensed for now. This is a personal learning project.
