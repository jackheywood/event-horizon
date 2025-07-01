from events import deserialize_event


def main():
    events = [
        deserialize_event({
            "type": "LightSwitchedOff",
            "light_id": "Fairy",
            "timestamp": "2025-07-01T17:20:40"
        }),
        deserialize_event({
            "type": "LightSwitchedOn",
            "light_id": "Fairy",
            "timestamp": "2025-08-01T17:00:00"
        }),
    ]

    for event in events:
        print(event)


if __name__ == "__main__":
    main()
