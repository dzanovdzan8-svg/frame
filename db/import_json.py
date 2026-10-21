"""Однократный перенос данных из JSON-файлов в таблицы SQLite."""
import json
import sqlite3
from pathlib import Path

from db.database import BASE_DIR, get_connection, init_schema

DATA_DIR = BASE_DIR / "data"


def load_json(filename: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_trips(conn: sqlite3.Connection, data_dir: Path) -> None:
    """Перенести поездки из trips.json в таблицу trips."""
    trips = load_json(data_dir / "trips.json")
    conn.executemany(
        """
        INSERT INTO trips (id, title, country, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            country = excluded.country,
            start_date = excluded.start_date,
            end_date = excluded.end_date
        """,
        [
            (
                trip["id"],
                trip["title"],
                trip["country"],
                trip["start_date"],
                trip["end_date"],
            )
            for trip in trips
        ],
    )


def import_travelers(conn: sqlite3.Connection, data_dir: Path) -> None:
    """Перенести путешественников из travelers.json."""
    travelers = load_json(data_dir / "travelers.json")
    conn.executemany(
        """
        INSERT INTO travelers (id, name, email)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            email = excluded.email
        """,
        [(t["id"], t["name"], t["email"]) for t in travelers],
    )


def import_notes(conn: sqlite3.Connection, data_dir: Path) -> None:
    """Перенести заметки из notes.json (после поездок и авторов)."""
    notes = load_json(data_dir / "notes.json")
    conn.executemany(
        """
        INSERT INTO notes (
            id, trip_id, traveler_id, note_date, text, is_archived
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            trip_id = excluded.trip_id,
            traveler_id = excluded.traveler_id,
            note_date = excluded.note_date,
            text = excluded.text,
            is_archived = excluded.is_archived
        """,
        [
            (
                note["id"],
                note["trip_id"],
                note["traveler_id"],
                note["note_date"],
                note.get("text", ""),
                int(note.get("is_archived", False)),
            )
            for note in notes
        ],
    )


def import_all(conn: sqlite3.Connection, data_dir: Path = DATA_DIR) -> None:
    """Импортировать все данные; порядок важен из-за внешних ключей."""
    import_trips(conn, data_dir)
    import_travelers(conn, data_dir)
    import_notes(conn, data_dir)


def main() -> None:
    """Создать схему и перенести данные одной транзакцией."""
    conn = get_connection()
    try:
        init_schema(conn)
        import_all(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
