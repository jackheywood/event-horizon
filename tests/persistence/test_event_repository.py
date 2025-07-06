import pytest

from event_horizon.persistence import EventRepository


@pytest.fixture
def event_repo(tmp_path):
    temp_file = tmp_path / "event_log.jsonl"
    return EventRepository(str(temp_file))


@pytest.fixture
def category():
    return "LightEvent"


@pytest.fixture
def kitchen_events(category):
    return [
        {
            "category": category,
            "type": "LightCreated",
            "aggregate_id": "kitchen",
            "timestamp": "2025-07-01T17:20:40",
            "is_on": True,
        },
        {
            "category": category,
            "type": "LightSwitchedOff",
            "aggregate_id": "kitchen",
            "timestamp": "2025-07-03T17:20:40",
        },
    ]


@pytest.fixture
def bedroom_events(category):
    return [
        {
            "category": category,
            "type": "LightCreated",
            "aggregate_id": "bedroom",
            "timestamp": "2025-07-02T17:20:40",
            "is_on": False,
        },
    ]


@pytest.fixture
def events(kitchen_events, bedroom_events):
    return [
        kitchen_events[0],
        bedroom_events[0],
        {
            "category": "OtherEvent",
            "type": "OtherType",
            "aggregate_id": "lounge",
            "timestamp": "2025-07-03T12:00:00",
        },
        kitchen_events[1],
    ]


def test_save_and_load(event_repo, category, events, kitchen_events, bedroom_events):
    # Act
    for event in events:
        event_repo.save(event)

    loaded_kitchen_events = list(event_repo.load(category, "kitchen"))
    loaded_bedroom_events = list(event_repo.load(category, "bedroom"))

    # Assert
    assert loaded_kitchen_events == kitchen_events
    assert loaded_bedroom_events == bedroom_events


def test_load_empty_file(event_repo, category):
    # Act
    loaded_events = list(event_repo.load(category, "kitchen"))

    # Assert
    assert loaded_events == []


def test_load_all(event_repo, category, events, kitchen_events, bedroom_events):
    # Arrange
    for event in events:
        event_repo.save(event)

    # Act
    loaded_events = event_repo.load_all(category)

    # Assert
    assert loaded_events == {
        "kitchen": kitchen_events,
        "bedroom": bedroom_events,
    }


def test_load_all_empty_file(event_repo, category):
    # Act
    loaded_events = event_repo.load_all(category)

    # Assert
    assert loaded_events == {}
