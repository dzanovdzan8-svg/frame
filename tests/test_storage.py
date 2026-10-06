import json

from models import Traveler, Trip
from models.notes import create_note
from storage import (
    load_notes,
    load_trips,
    save_notes,
    save_trips,
)


def test_trips_roundtrip(tmp_path):
    path = tmp_path / "trips.json"
    trips = [Trip(1, "Байкал", "Россия", "2026-07-10", "2026-07-17")]
    save_trips(str(path), trips)
    loaded = load_trips(str(path))
    assert loaded[0].to_data() == trips[0].to_data()


def test_notes_saved_as_ids_and_restored_as_objects(tmp_path):
    path = tmp_path / "notes.json"
    trip = Trip(1, "Байкал", "Россия", "2026-07-10", "2026-07-17")
    anna = Traveler(1, "Анна", "anna@example.com")
    notes = []
    create_note(notes, trip, "2026-07-12", anna, "Закат")
    save_notes(str(path), notes)
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw[0]["trip_id"] == 1
    assert raw[0]["traveler_id"] == 1
    loaded = load_notes(str(path), [trip], [anna])
    assert loaded[0].trip is trip
    assert loaded[0].traveler is anna


def test_missing_and_broken_files(tmp_path):
    assert load_trips(str(tmp_path / "none.json")) == []
    broken = tmp_path / "broken.json"
    broken.write_text("{не json", encoding="utf-8")
    assert load_trips(str(broken)) == []


def test_note_with_unknown_trip_is_skipped(tmp_path):
    path = tmp_path / "notes.json"
    path.write_text(json.dumps([
        {"id": 1, "trip_id": 9, "note_date": "2026-07-12",
         "traveler_id": 1, "text": ""},
    ]), encoding="utf-8")
    assert load_notes(str(path), [], []) == []
