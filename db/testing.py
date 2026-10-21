"""Вспомогательные средства для тестов: временная база данных."""
import sqlite3
import tempfile
from pathlib import Path
from unittest import mock

from db import database
from db.import_json import DATA_DIR, import_all


def use_test_database(testcase, with_data: bool = True) -> Path:
    """Подменить базу проекта временной на время теста."""
    tmp = tempfile.TemporaryDirectory()
    testcase.addCleanup(tmp.cleanup)
    path = Path(tmp.name) / "test.sqlite"

    patcher = mock.patch.object(database, "DB_PATH", path)
    patcher.start()
    testcase.addCleanup(patcher.stop)

    conn = sqlite3.connect(path)
    database.init_schema(conn)
    if with_data:
        import_all(conn, DATA_DIR)
    conn.commit()
    conn.close()
    return path
