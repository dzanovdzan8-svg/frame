"""Класс Trip и функции работы с коллекцией поездок."""
from datetime import date
from typing import List, Optional


class Trip:
    """Поездка (маршрут) путешественника."""

    def __init__(
        self,
        trip_id: int,
        title: str,
        country: str,
        start_date: str,
        end_date: str,
    ) -> None:
        """Создать объект поездки (даты - строки ISO: ГГГГ-ММ-ДД)."""
        self.id = trip_id
        self.title = title
        self.country = country
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> bool:
        """Проверить, что дата окончания не раньше даты начала."""
        return date.fromisoformat(start_date) <= date.fromisoformat(end_date)

    @classmethod
    def from_data(cls, data: dict) -> "Trip":
        """Создать поездку из словаря JSON."""
        return cls(
            trip_id=data["id"],
            title=data["title"],
            country=data["country"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        )

    def to_data(self) -> dict:
        """Вернуть данные поездки для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "country": self.country,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    @property
    def duration_days(self) -> int:
        """Длительность поездки в днях (включая крайние дни)."""
        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)
        return (end - start).days + 1

    def lasts_at_least(self, days: int) -> bool:
        """Проверить, что поездка длится не меньше days дней."""
        return self.duration_days >= days

    def includes_day(self, day: str) -> bool:
        """Проверить, что день (строка ISO) входит в период поездки."""
        return self.start_date <= day <= self.end_date

    def __str__(self) -> str:
        """Строковое представление поездки."""
        return (
            f"{self.title} ({self.country}), "
            f"{self.start_date} - {self.end_date}, "
            f"{self.duration_days} дн."
        )


def add_trip(
    trips: List[Trip],
    title: str,
    country: str,
    start_date: str,
    end_date: str,
) -> Trip:
    """Создать объект Trip, добавить в коллекцию и вернуть его."""
    if not Trip.validate_dates(start_date, end_date):
        raise ValueError("Дата окончания раньше даты начала")
    trip = Trip(
        max((t.id for t in trips), default=0) + 1,
        title,
        country,
        start_date,
        end_date,
    )
    trips.append(trip)
    return trip


def find_trip(trips: List[Trip], query: str) -> List[Trip]:
    """Найти поездки по подстроке названия (без учёта регистра)."""
    query = query.lower()
    return [trip for trip in trips if query in trip.title.lower()]


def find_trip_by_id(trips: List[Trip], trip_id: int) -> Optional[Trip]:
    """Найти поездку по идентификатору."""
    for trip in trips:
        if trip.id == trip_id:
            return trip
    return None


def check_trip_duration(
    trips: List[Trip],
    trip_id: int,
    min_days: int,
) -> bool:
    """Найти поездку и проверить её длительность."""
    trip = find_trip_by_id(trips, trip_id)
    if trip is None:
        return False
    return trip.lasts_at_least(min_days)


def filter_trips_by_duration(
    trips: List[Trip],
    min_days: int,
) -> List[Trip]:
    """Отобрать поездки длительностью не меньше min_days дней."""
    return [trip for trip in trips if trip.lasts_at_least(min_days)]


def sort_trips(trips: List[Trip]) -> List[Trip]:
    """Вернуть поездки, упорядоченные по длительности."""
    return sorted(trips, key=lambda trip: trip.duration_days)


def show_trips(trips: List[Trip]) -> None:
    """Вывести информацию о поездках."""
    if not trips:
        print("Поездок нет")
    for trip in trips:
        print(f"{trip.id}. {trip}")
