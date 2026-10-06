"""Вспомогательные функции безопасного ввода."""
from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запрашивать целое число, пока ввод не станет корректным."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Нужно ввести целое число")


def input_date(prompt: str) -> date:
    """Запрашивать дату в формате ДД.ММ.ГГГГ до корректного ввода."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Неверная дата, формат: ДД.ММ.ГГГГ")
