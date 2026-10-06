"""Функции для работы с заметками (данные - словари)."""
from datetime import date


def is_day_free(
    notes: list[dict],
    trip_id: int,
    note_date: date,
) -> bool:
    """Проверить, что на день поездки ещё нет заметки."""
    iso = note_date.isoformat()
    for note in notes:
        if note["trip_id"] == trip_id and note["note_date"] == iso:
            return False
    return True


def create_note(
    notes: list[dict],
    trip_id: int,
    note_date: date,
    text: str = "",
) -> dict:
    """Создать заметку; на один день поездки - одна заметка."""
    if not is_day_free(notes, trip_id, note_date):
        raise ValueError("На этот день заметка уже есть")
    note = {
        "id": max((n["id"] for n in notes), default=0) + 1,
        "trip_id": trip_id,
        "note_date": note_date.isoformat(),
        "text": text,
    }
    notes.append(note)
    return note


def archive_note(notes: list[dict], note_id: int) -> bool:
    """Убрать заметку из списка; вернуть False, если её нет."""
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return True
    return False


def get_note_status(day_in_trip: bool, has_note_for_day: bool) -> str:
    """Вернуть текстовый статус дня (функция из ПР1)."""
    if not day_in_trip:
        return "Этот день не входит в период поездки"
    if has_note_for_day:
        return "На этот день заметка уже есть"
    return "Можно добавить заметку"
