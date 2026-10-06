"""Консольное приложение «Путевые заметки» (ПР2)."""
from datetime import date

from trips import (
    add_trip,
    check_trip_duration,
    find_trip,
    is_day_in_trip,
    sort_trips,
    trip_days,
)
from notes import (
    archive_note,
    create_note,
    get_note_status,
    is_day_free,
)
from storage import load_notes, load_trips, save_notes, save_trips
from utils import input_date, input_int

TRIPS_FILE = "data/trips.json"
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
0. Выход"""


def show_trips(trips: list[dict]) -> None:
    """Вывести список поездок."""
    if not trips:
        print("Поездок нет")
    for trip in trips:
        print(
            f"{trip['id']}. {trip['title']} ({trip['country']}), "
            f"{trip['start_date']} - {trip['end_date']}, "
            f"{trip_days(trip)} дн."
        )


def show_notes(notes: list[dict], trips: dict[int, dict]) -> None:
    """Вывести список заметок с названиями поездок."""
    if not notes:
        print("Заметок нет")
    for note in notes:
        trip = trips.get(note["trip_id"], {"title": "?"})
        print(f"{note['id']}. {trip['title']} - {note['note_date']}: "
              f"{note['text']}")


def select_trip(trips: dict[int, dict]) -> dict | None:
    """Запросить id поездки и вернуть её данные или None."""
    trip = trips.get(input_int("ID поездки: "))
    if trip is None:
        print("Поездка не найдена")
    return trip


def check_day(trips: dict[int, dict], notes: list[dict]) -> None:
    """Сценарий: проверить, можно ли добавить заметку на день."""
    trip = select_trip(trips)
    if trip is None:
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    in_trip = is_day_in_trip(
        day,
        _iso(trip["start_date"]),
        _iso(trip["end_date"]),
    )
    print(get_note_status(in_trip, not is_day_free(notes, trip["id"], day)))


def _iso(value: str) -> date:
    """Преобразовать строку ISO в дату."""
    return date.fromisoformat(value)


def add_note(trips: dict[int, dict], notes: list[dict]) -> None:
    """Сценарий: добавить заметку к дню поездки."""
    trip = select_trip(trips)
    if trip is None:
        return
    day = input_date("Дата (ДД.ММ.ГГГГ): ")
    if not is_day_in_trip(
        day, _iso(trip["start_date"]), _iso(trip["end_date"])
    ):
        print("Этот день не входит в период поездки")
        return
    text = input("Текст заметки: ")
    try:
        note = create_note(notes, trip["id"], day, text)
    except ValueError as error:
        print(error)
        return
    print(f"Заметка №{note['id']} добавлена")


def main() -> None:
    """Точка запуска: цикл меню."""
    trips = load_trips(TRIPS_FILE)
    notes = load_notes(NOTES_FILE)
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_trips(list(trips.values()))
        elif choice == "2":
            show_trips(find_trip(trips, input("Часть названия: ")))
        elif choice == "3":
            trip = select_trip(trips)
            if trip:
                days = input_int("Минимум дней: ")
                ok = check_trip_duration(trips, trip["id"], days)
                print("Подходит" if ok else "Поездка короче")
        elif choice == "4":
            check_day(trips, notes)
        elif choice == "5":
            add_note(trips, notes)
        elif choice == "6":
            done = archive_note(notes, input_int("ID заметки: "))
            print("Заметка архивирована" if done else "Заметка не найдена")
        elif choice == "7":
            show_notes(notes, trips)
        elif choice == "8":
            add_new_trip(trips)
        elif choice == "9":
            show_trips(sort_trips(trips))
        elif choice == "0":
            break
        else:
            print("Неизвестный пункт меню")
    save_trips(TRIPS_FILE, trips)
    save_notes(NOTES_FILE, notes)


def add_new_trip(trips: dict[int, dict]) -> None:
    """Сценарий: добавить новую поездку."""
    title = input("Название: ")
    country = input("Страна: ")
    start = input_date("Начало (ДД.ММ.ГГГГ): ")
    end = input_date("Окончание (ДД.ММ.ГГГГ): ")
    try:
        trip = add_trip(trips, title, country, start, end)
    except ValueError as error:
        print(error)
        return
    print(f"Поездка №{trip['id']} добавлена")


if __name__ == "__main__":
    main()
