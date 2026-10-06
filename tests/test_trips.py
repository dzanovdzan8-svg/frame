from datetime import date

import pytest

from trips import (
    add_trip,
    check_trip_duration,
    filter_trips_by_duration,
    find_trip,
    sort_trips,
)


def make_trips():
    trips = {}
    add_trip(trips, "Байкал", "Россия", date(2026, 7, 10), date(2026, 7, 17))
    add_trip(trips, "Стамбул", "Турция", date(2026, 9, 4), date(2026, 9, 6))
    return trips


def test_add_trip():
    trips = {}
    add_trip(trips, "Байкал", "Россия", date(2026, 7, 10), date(2026, 7, 17))
    assert len(trips) == 1
    assert trips[1]["title"] == "Байкал"


def test_add_trip_wrong_dates():
    with pytest.raises(ValueError):
        add_trip({}, "X", "Y", date(2026, 7, 10), date(2026, 7, 1))


def test_find_trip_ignores_case():
    assert len(find_trip(make_trips(), "байкал")) == 1


def test_check_trip_duration():
    trips = make_trips()
    assert check_trip_duration(trips, 1, 5)
    assert not check_trip_duration(trips, 2, 5)
    assert not check_trip_duration(trips, 99, 1)


def test_filter_and_sort_trips():
    trips = make_trips()
    assert [t["id"] for t in filter_trips_by_duration(trips, 5)] == [1]
    assert [t["id"] for t in sort_trips(trips)] == [2, 1]
