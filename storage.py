"""Загрузка и сохранение данных: JSON <-> объекты."""
import json
import logging
from typing import List

from models.notes import Note
from models.travelers import Traveler, find_traveler_by_id
from models.trips import Trip, find_trip_by_id

logger = logging.getLogger(__name__)


def _read_json(filename: str) -> List[dict]:
    """Прочитать список записей из JSON; при ошибке вернуть []."""
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.warning("Файл %s не найден, начинаем с пустых данных",
                       filename)
        return []
    except json.JSONDecodeError:
        logger.warning("Файл %s содержит некорректный JSON", filename)
        return []
    if not isinstance(data, list):
        logger.warning("Файл %s: ожидался список записей", filename)
        return []
    return data


def _write_json(filename: str, data: List[dict]) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_trips(filename: str) -> List[Trip]:
    """Загрузить поездки: JSON -> объекты Trip."""
    return [Trip.from_data(item) for item in _read_json(filename)]


def save_trips(filename: str, trips: List[Trip]) -> None:
    """Сохранить поездки: объекты Trip -> JSON."""
    _write_json(filename, [trip.to_data() for trip in trips])


def load_travelers(filename: str) -> List[Traveler]:
    """Загрузить путешественников: JSON -> объекты Traveler."""
    return [Traveler.from_data(item) for item in _read_json(filename)]


def save_travelers(filename: str, travelers: List[Traveler]) -> None:
    """Сохранить путешественников: объекты Traveler -> JSON."""
    _write_json(filename, [t.to_data() for t in travelers])


def load_notes(
    filename: str,
    trips: List[Trip],
    travelers: List[Traveler],
) -> List[Note]:
    """Загрузить заметки, восстановив связи с Trip и Traveler."""
    notes: List[Note] = []
    for item in _read_json(filename):
        trip = find_trip_by_id(trips, item["trip_id"])
        traveler = find_traveler_by_id(travelers, item["traveler_id"])
        if trip is None or traveler is None:
            logger.warning("Заметка %s пропущена: нет связанных объектов",
                           item.get("id"))
            continue
        note = Note(
            item["id"],
            trip,
            item["note_date"],
            traveler,
            item.get("text", ""),
        )
        note.is_archived = item.get("is_archived", False)
        notes.append(note)
    return notes


def save_notes(filename: str, notes: List[Note]) -> None:
    """Сохранить заметки: объекты связей -> идентификаторы."""
    _write_json(filename, [note.to_data() for note in notes])
