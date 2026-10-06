from datetime import date

import pytest

from notes import (
    archive_note,
    create_note,
    get_note_status,
    is_day_free,
)


def test_is_day_free_on_empty_list():
    assert is_day_free([], 1, date(2026, 7, 12))


def test_duplicate_note_forbidden():
    notes = []
    create_note(notes, 1, date(2026, 7, 12), "Первый день")
    assert not is_day_free(notes, 1, date(2026, 7, 12))
    with pytest.raises(ValueError):
        create_note(notes, 1, date(2026, 7, 12), "Ещё одна")


def test_same_day_other_trip_is_free():
    notes = []
    create_note(notes, 1, date(2026, 7, 12))
    assert is_day_free(notes, 2, date(2026, 7, 12))


def test_archive_note():
    notes = []
    note = create_note(notes, 1, date(2026, 7, 12))
    assert archive_note(notes, note["id"])
    assert not archive_note(notes, note["id"])
    assert is_day_free(notes, 1, date(2026, 7, 12))


def test_get_note_status():
    assert get_note_status(True, False) == "Можно добавить заметку"
    assert "уже есть" in get_note_status(True, True)
    assert "не входит" in get_note_status(False, False)
