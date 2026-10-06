"""Класс Note и функции работы с коллекцией заметок."""
from typing import List, Optional

from .travelers import Traveler
from .trips import Trip


class Note:
    """Заметка о дне поездки."""

    def __init__(
        self,
        note_id: int,
        trip: Trip,
        note_date: str,
        traveler: Traveler,
        text: str = "",
    ) -> None:
        """Создать заметку, связав её с поездкой и автором."""
        self.id = note_id
        self.trip = trip
        self.note_date = note_date
        self.traveler = traveler
        self.text = text
        self.is_archived = False

    def archive(self) -> None:
        """Архивировать заметку (объект остаётся в коллекции)."""
        self.is_archived = True

    def to_data(self) -> dict:
        """Вернуть данные для JSON: объекты заменяются идентификаторами."""
        return {
            "id": self.id,
            "trip_id": self.trip.id,
            "note_date": self.note_date,
            "traveler_id": self.traveler.id,
            "text": self.text,
            "is_archived": self.is_archived,
        }

    def __str__(self) -> str:
        """Строковое представление заметки с учётом состояния."""
        state = "архив" if self.is_archived else "активна"
        return (
            f"Заметка №{self.id}: {self.trip.title}, {self.note_date}, "
            f"автор {self.traveler.name} [{state}]"
        )


def is_day_free(
    notes: List[Note],
    trip: Trip,
    note_date: str,
) -> bool:
    """Проверить, что на день поездки нет активной заметки."""
    for note in notes:
        if (
            note.trip.id == trip.id
            and note.note_date == note_date
            and not note.is_archived
        ):
            return False
    return True


def create_note(
    notes: List[Note],
    trip: Trip,
    note_date: str,
    traveler: Traveler,
    text: str = "",
) -> Optional[Note]:
    """Создать заметку; None, если на этот день уже есть активная."""
    if not is_day_free(notes, trip, note_date):
        return None
    note = Note(
        max((n.id for n in notes), default=0) + 1,
        trip,
        note_date,
        traveler,
        text,
    )
    notes.append(note)
    return note


def find_note_by_id(notes: List[Note], note_id: int) -> Optional[Note]:
    """Найти заметку по идентификатору."""
    for note in notes:
        if note.id == note_id:
            return note
    return None


def archive_note(notes: List[Note], note_id: int) -> bool:
    """Найти заметку и архивировать её; False, если не найдена."""
    note = find_note_by_id(notes, note_id)
    if note is None or note.is_archived:
        return False
    note.archive()
    return True


def get_note_status(day_in_trip: bool, day_is_free: bool) -> str:
    """Вернуть текстовый статус дня (функция из ПР1)."""
    if not day_in_trip:
        return "Этот день не входит в период поездки"
    if not day_is_free:
        return "На этот день заметка уже есть"
    return "Можно добавить заметку"


def show_notes(notes: List[Note]) -> None:
    """Вывести информацию о заметках."""
    if not notes:
        print("Заметок нет")
    for note in notes:
        print(f"{note}\n    {note.text}")
