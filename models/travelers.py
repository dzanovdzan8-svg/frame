"""Класс Traveler и функции работы с коллекцией путешественников."""
from typing import List, Optional


class Traveler:
    """Путешественник - автор заметок."""

    def __init__(self, traveler_id: int, name: str, email: str) -> None:
        """Создать объект путешественника."""
        self.id = traveler_id
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Traveler":
        """Создать путешественника из словаря JSON."""
        return cls(data["id"], data["name"], data["email"])

    def to_data(self) -> dict:
        """Вернуть данные для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        """Строковое представление путешественника."""
        return f"{self.name} <{self.email}>"


def add_traveler(
    travelers: List[Traveler],
    name: str,
    email: str,
) -> Traveler:
    """Создать объект Traveler и добавить в коллекцию."""
    traveler = Traveler(
        max((t.id for t in travelers), default=0) + 1,
        name,
        email,
    )
    travelers.append(traveler)
    return traveler


def find_traveler(
    travelers: List[Traveler],
    query: str,
) -> List[Traveler]:
    """Найти путешественников по имени или адресу почты."""
    query = query.lower()
    return [
        t for t in travelers
        if query in t.name.lower() or query in t.email.lower()
    ]


def find_traveler_by_id(
    travelers: List[Traveler],
    traveler_id: int,
) -> Optional[Traveler]:
    """Найти путешественника по идентификатору."""
    for traveler in travelers:
        if traveler.id == traveler_id:
            return traveler
    return None


def show_travelers(travelers: List[Traveler]) -> None:
    """Вывести информацию о путешественниках."""
    if not travelers:
        print("Путешественников нет")
    for traveler in travelers:
        print(f"{traveler.id}. {traveler}")
