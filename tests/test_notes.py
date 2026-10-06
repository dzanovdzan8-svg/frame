from models import Note, Traveler, Trip
from models.notes import (
    archive_note,
    create_note,
    find_note_by_id,
    get_note_status,
    is_day_free,
)


def make_objects():
    trip = Trip(1, "Байкал", "Россия", "2026-07-10", "2026-07-17")
    anna = Traveler(1, "Анна", "anna@example.com")
    ivan = Traveler(2, "Иван", "ivan@example.com")
    return trip, anna, ivan


def test_note_creation():
    trip, anna, _ = make_objects()
    note = Note(1, trip, "2026-07-12", anna, "Закат")
    assert note.id == 1
    assert note.trip is trip
    assert note.traveler is anna
    assert note.note_date == "2026-07-12"
    assert not note.is_archived


def test_note_archive_and_str():
    trip, anna, _ = make_objects()
    note = Note(1, trip, "2026-07-12", anna)
    assert "активна" in str(note)
    note.archive()
    assert note.is_archived
    assert "архив" in str(note)


def test_second_active_note_not_created():
    trip, anna, ivan = make_objects()
    notes = []
    first = create_note(notes, trip, "2026-07-12", anna, "Первая")
    second = create_note(notes, trip, "2026-07-12", ivan, "Вторая")
    assert first is not None
    assert second is None
    assert len(notes) == 1


def test_archived_note_does_not_block_day():
    trip, anna, ivan = make_objects()
    notes = []
    first = create_note(notes, trip, "2026-07-12", anna)
    first.archive()
    assert is_day_free(notes, trip, "2026-07-12")
    again = create_note(notes, trip, "2026-07-12", ivan)
    assert again is not None
    assert len(notes) == 2


def test_archive_note_keeps_object_in_collection():
    trip, anna, _ = make_objects()
    notes = []
    note = create_note(notes, trip, "2026-07-12", anna)
    assert archive_note(notes, note.id)
    assert notes == [note]
    assert not archive_note(notes, note.id)
    assert not archive_note(notes, 99)
    assert find_note_by_id(notes, note.id) is note


def test_get_note_status():
    assert get_note_status(True, True) == "Можно добавить заметку"
    assert "уже есть" in get_note_status(True, False)
    assert "не входит" in get_note_status(False, True)
