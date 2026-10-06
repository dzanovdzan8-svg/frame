import pytest

from models import Trip
from models.trips import (
    add_trip,
    check_trip_duration,
    filter_trips_by_duration,
    find_trip,
    find_trip_by_id,
    sort_trips,
)


def make_trips():
    return [
        Trip(1, "Байкал", "Россия", "2026-07-10", "2026-07-17"),
        Trip(2, "Стамбул", "Турция", "2026-09-04", "2026-09-06"),
    ]


def test_trip_creation():
    trip = make_trips()[0]
    assert trip.id == 1
    assert trip.title == "Байкал"
    assert trip.duration_days == 8


def test_trip_str():
    assert "Байкал" in str(make_trips()[0])
    assert "8 дн." in str(make_trips()[0])


def test_lasts_at_least_and_includes_day():
    trip = make_trips()[1]
    assert trip.lasts_at_least(3)
    assert not trip.lasts_at_least(4)
    assert trip.includes_day("2026-09-05")
    assert not trip.includes_day("2026-09-07")


def test_validate_dates_static():
    assert Trip.validate_dates("2026-01-01", "2026-01-02")
    assert not Trip.validate_dates("2026-01-02", "2026-01-01")


def test_from_data_and_to_data():
    data = make_trips()[0].to_data()
    assert Trip.from_data(data).to_data() == data


def test_add_trip_to_collection():
    trips = []
    trip = add_trip(trips, "Алтай", "Россия", "2026-08-01", "2026-08-05")
    assert trips == [trip]
    assert trip.id == 1


def test_add_trip_wrong_dates():
    with pytest.raises(ValueError):
        add_trip([], "X", "Y", "2026-08-05", "2026-08-01")


def test_find_filter_sort():
    trips = make_trips()
    assert find_trip(trips, "байкал") == [trips[0]]
    assert find_trip_by_id(trips, 2) is trips[1]
    assert find_trip_by_id(trips, 99) is None
    assert filter_trips_by_duration(trips, 5) == [trips[0]]
    assert sort_trips(trips) == [trips[1], trips[0]]


def test_check_trip_duration():
    trips = make_trips()
    assert check_trip_duration(trips, 1, 5)
    assert not check_trip_duration(trips, 2, 5)
    assert not check_trip_duration(trips, 99, 1)
