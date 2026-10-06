"""Загрузка и сохранение данных в JSON-файлах."""
import json
import logging

logger = logging.getLogger(__name__)


def _read_json(filename: str) -> list[dict]:
    """Прочитать список записей из JSON; при ошибке вернуть []."""
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.warning("Файл %s не найден, начинаем с пустых данных",
                       filename)
        return []
    except json.JSONDecodeError:
        logger.warning("Файл %s содержит некорректный JSON", filename)
        return []
    if not isinstance(data, list):
        logger.warning("Файл %s: ожидался список записей", filename)
        return []
    return data


def _write_json(filename: str, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_trips(filename: str) -> dict[int, dict]:
    """Загрузить поездки из JSON в словарь {id: данные}."""
    return {item["id"]: item for item in _read_json(filename)}


def save_trips(filename: str, trips: dict[int, dict]) -> None:
    """Сохранить поездки в JSON-файл."""
    _write_json(filename, list(trips.values()))


def load_notes(filename: str) -> list[dict]:
    """Загрузить заметки из JSON-файла."""
    return _read_json(filename)


def save_notes(filename: str, notes: list[dict]) -> None:
    """Сохранить заметки в JSON-файл."""
    _write_json(filename, notes)
