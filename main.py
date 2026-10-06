"""Консольное приложение «Путевые заметки» (объектная модель, ПР3)."""
from typing import List, Optional

from models import Note, Traveler, Trip
from models.notes import (
    archive_note,
    create_note,
    get_note_status,
    is_day_free,
    show_notes,
)
from models.travelers import (
    add_traveler,
    find_traveler,
    find_traveler_by_id,
    show_travelers,
)
from models.trips import (
    add_trip,
    check_trip_duration,
    find_trip,
    find_trip_by_id,
    show_trips,
    sort_trips,
)
from storage import (
    load_notes,
    load_travelers,
    load_trips,
    save_notes,
    save_travelers,
    save_trips,
)
from utils import input_date, input_int

TRIPS_FILE = "data/trips.json"
TRAVELERS_FILE = "data/travelers.json"
NOTES_FILE = "data/notes.json"

MENU = """
=== Путевые заметки ===
1. Показать поездки
2. Найти поездку по названию
3. Проверить длительность поездки
4. Проверить, свободен ли день для заметки
5. Добавить заметку
6. Архивировать заметку
7. Показать заметки
8. Добавить поездку
9. Отсортировать поездки по длительности
10. Показать путешественников
11. Найти путешественника
12. Добавить путешественника
0. Выход"""


def select_trip(trips: List[Trip]) -> Optional[Trip]:
    """Запросить id поездки и вернуть объект Trip или None."""
    trip = find_trip_by_id(trips, input_int("ID поездки: "))
    if trip is None:
        print("Поездка не найдена")
    return trip


def check_day(trips: List[Trip], notes: List[Note]) -> None:
    """Сценарий: проверить, можно ли добавить заметку на день."""
    trip = select_trip(trips)
    if trip is None:
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ").isoformat()
    print(get_note_status(trip.includes_day(day),
                          is_day_free(notes, trip, day)))


def create_new_note(
    notes: List[Note],
    trips: List[Trip],
    travelers: List[Traveler],
) -> None:
    """Сценарий: создать заметку, связав поездку и путешественника."""
    trip = select_trip(trips)
    if trip is None:
        return
    traveler = find_traveler_by_id(travelers, input_int("ID автора: "))
    if traveler is None:
        print("Путешественник не найден")
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ").isoformat()
    if not trip.includes_day(day):
        print("Этот день не входит в период поездки")
        return
    note = create_note(notes, trip, day, traveler, input("Текст: "))
    if note is None:
        print("На этот день заметка уже есть")
        return
    print(f"Заметка №{note.id} добавлена")


def add_new_trip(trips: List[Trip]) -> None:
    """Сценарий: добавить новую поездку."""
    title = input("Название: ")
    country = input("Страна: ")
    start = input_date("Начало (ДД.ММ.ГГГГ): ").isoformat()
    end = input_date("Окончание (ДД.ММ.ГГГГ): ").isoformat()
    try:
        trip = add_trip(trips, title, country, start, end)
    except ValueError as error:
        print(error)
        return
    print(f"Поездка №{trip.id} добавлена")


def check_duration(trips: List[Trip]) -> None:
    """Сценарий: проверить минимальную длительность поездки."""
    trip = select_trip(trips)
    if trip is None:
        return
    days = input_int("Минимум дней: ")
    ok = check_trip_duration(trips, trip.id, days)
    print("Подходит" if ok else "Поездка короче")


def main() -> None:
    """Точка запуска: загрузка данных, меню, сохранение."""
    trips = load_trips(TRIPS_FILE)
    travelers = load_travelers(TRAVELERS_FILE)
    notes = load_notes(NOTES_FILE, trips, travelers)
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_trips(trips)
        elif choice == "2":
            show_trips(find_trip(trips, input("Часть названия: ")))
        elif choice == "3":
            check_duration(trips)
        elif choice == "4":
            check_day(trips, notes)
        elif choice == "5":
            create_new_note(notes, trips, travelers)
        elif choice == "6":
            done = archive_note(notes, input_int("ID заметки: "))
            print("Заметка архивирована" if done else "Заметка не найдена")
        elif choice == "7":
            show_notes(notes)
        elif choice == "8":
            add_new_trip(trips)
        elif choice == "9":
            show_trips(sort_trips(trips))
        elif choice == "10":
            show_travelers(travelers)
        elif choice == "11":
            found = find_traveler(travelers, input("Имя или e-mail: "))
            show_travelers(found)
        elif choice == "12":
            traveler = add_traveler(
                travelers,
                input("Имя: "),
                input("E-mail: "),
            )
            print(f"Путешественник №{traveler.id} добавлен")
        elif choice == "0":
            break
        else:
            print("Неизвестный пункт меню")
    save_trips(TRIPS_FILE, trips)
    save_travelers(TRAVELERS_FILE, travelers)
    save_notes(NOTES_FILE, notes)


if __name__ == "__main__":
    main()
