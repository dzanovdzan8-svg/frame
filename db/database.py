"""Подключение к базе данных SQLite проекта «Путевые заметки»."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "travelnotes.sqlite"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    """Открыть соединение с базой и включить проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    """Создать таблицы из sql/schema.sql (повторный запуск безопасен)."""
    sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(sql)
