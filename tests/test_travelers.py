from models import Traveler
from models.travelers import (
    add_traveler,
    find_traveler,
    find_traveler_by_id,
)


def test_traveler_creation():
    traveler = Traveler(1, "Иван Петров", "ivan@example.com")
    assert traveler.id == 1
    assert traveler.name == "Иван Петров"
    assert traveler.email == "ivan@example.com"


def test_traveler_str():
    traveler = Traveler(1, "Иван Петров", "ivan@example.com")
    assert str(traveler) == "Иван Петров <ivan@example.com>"


def test_from_data():
    data = {"id": 2, "name": "Анна", "email": "anna@example.com"}
    traveler = Traveler.from_data(data)
    assert traveler.to_data() == data


def test_add_and_find_traveler():
    travelers = []
    add_traveler(travelers, "Анна Смирнова", "anna@example.com")
    add_traveler(travelers, "Иван Петров", "ivan@example.com")
    assert [t.id for t in travelers] == [1, 2]
    assert len(find_traveler(travelers, "анна")) == 1
    assert len(find_traveler(travelers, "example.com")) == 2
    assert find_traveler_by_id(travelers, 2).name == "Иван Петров"
    assert find_traveler_by_id(travelers, 9) is None
