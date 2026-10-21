import json
import sqlite3

import pytest

from db import database
from db.import_json import DATA_DIR, import_all


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "test.sqlite")
    connection.execute("PRAGMA foreign_keys = ON")
    database.init_schema(connection)
    connection.row_factory = sqlite3.Row
    yield connection
    connection.close()


def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def json_count(name):
    with open(DATA_DIR / name, encoding="utf-8") as file:
        return len(json.load(file))


def test_schema_creates_tables(conn):
    names = {
        row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    assert {"trips", "travelers", "notes"} <= names


def test_schema_can_run_twice(conn):
    database.init_schema(conn)


def test_notes_have_foreign_keys(conn):
    tables = {
        row["table"] for row in conn.execute(
            "PRAGMA foreign_key_list(notes)"
        )
    }
    assert tables == {"trips", "travelers"}


def test_foreign_key_is_enforced(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO notes (id, trip_id, traveler_id, note_date) "
            "VALUES (1, 999, 999, '2026-07-12')"
        )


def test_import_matches_json_counts(conn):
    import_all(conn, DATA_DIR)
    assert count(conn, "trips") == json_count("trips.json")
    assert count(conn, "travelers") == json_count("travelers.json")
    assert count(conn, "notes") == json_count("notes.json")


def test_import_is_repeatable(conn):
    import_all(conn, DATA_DIR)
    import_all(conn, DATA_DIR)
    assert count(conn, "notes") == json_count("notes.json")


def test_one_active_note_per_day(conn):
    import_all(conn, DATA_DIR)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO notes (id, trip_id, traveler_id, note_date) "
            "VALUES (100, 1, 1, '2026-07-12')"
        )


def test_archived_note_does_not_block_day(conn):
    import_all(conn, DATA_DIR)
    conn.execute("UPDATE notes SET is_archived = 1 WHERE id = 1")
    conn.execute(
        "INSERT INTO notes (id, trip_id, traveler_id, note_date) "
        "VALUES (100, 1, 1, '2026-07-12')"
    )


def test_wrong_trip_dates_rejected(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO trips (id, title, country, start_date, end_date) "
            "VALUES (50, 'X', 'Y', '2026-07-10', '2026-07-01')"
        )


def test_parameter_is_not_executed_as_sql(conn):
    import_all(conn, DATA_DIR)
    evil = "2026-07-12' OR '1'='1"
    rows = conn.execute(
        "SELECT * FROM notes WHERE note_date = ?", [evil]
    ).fetchall()
    assert rows == []
    assert count(conn, "notes") == json_count("notes.json")


def read_queries():
    sql = (database.BASE_DIR / "sql" / "queries.sql").read_text(
        encoding="utf-8"
    )
    statements, buffer = [], []
    for line in sql.splitlines():
        buffer.append(line)
        if sqlite3.complete_statement("\n".join(buffer)):
            code = "\n".join(
                item for item in buffer if not item.strip().startswith("--")
            ).strip()
            buffer = []
            if code:
                statements.append(code)
    return statements


def test_queries_file_has_required_queries(conn):
    import_all(conn, DATA_DIR)
    statements = read_queries()
    assert len(statements) >= 10
    text = "\n".join(statements).upper()
    assert text.count("WHERE") >= 2
    assert text.count("JOIN") >= 2
    assert text.count("COUNT(") >= 2
    assert text.count("GROUP BY") >= 2
    assert "HAVING" in text
    for statement in statements:
        conn.execute(statement).fetchall()
