"""Функции для работы с поездками (данные - словари)."""
from datetime import date


def count_trip_days(start: date, end: date) -> int:
    """Вернуть длительность поездки в днях (из ПР1)."""
    return (end - start).days + 1


def is_day_in_trip(day: date, start: date, end: date) -> bool:
    """Проверить, что день входит в период поездки (из ПР1)."""
    return start <= day <= end


def trip_days(trip: dict) -> int:
    """Вернуть длительность поездки, заданной словарём."""
    return count_trip_days(
        date.fromisoformat(trip["start_date"]),
        date.fromisoformat(trip["end_date"]),
    )


def add_trip(
    trips: dict[int, dict],
    title: str,
    country: str,
    start_date: date,
    end_date: date,
) -> dict:
    """Добавить поездку в словарь trips и вернуть её данные."""
    if end_date < start_date:
        raise ValueError("Дата окончания раньше даты начала")
    trip_id = max(trips, default=0) + 1
    trips[trip_id] = {
        "id": trip_id,
        "title": title,
        "country": country,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    return trips[trip_id]


def find_trip(trips: dict[int, dict], query: str) -> list[dict]:
    """Найти поездки по подстроке названия (без учёта регистра)."""
    query = query.lower()
    return [
        trip for trip in trips.values()
        if query in trip["title"].lower()
    ]


def check_trip_duration(
    trips: dict[int, dict],
    trip_id: int,
    min_days: int,
) -> bool:
    """Проверить, что поездка длится не меньше min_days дней."""
    trip = trips.get(trip_id)
    if trip is None:
        return False
    return trip_days(trip) >= min_days


def filter_trips_by_duration(
    trips: dict[int, dict],
    min_days: int,
) -> list[dict]:
    """Отобрать поездки длительностью не меньше min_days дней."""
    return list(
        trip for trip in trips.values()
        if trip_days(trip) >= min_days
    )


def sort_trips(trips: dict[int, dict]) -> list[dict]:
    """Вернуть поездки, упорядоченные по длительности."""
    return sorted(trips.values(), key=lambda trip: trip_days(trip))
