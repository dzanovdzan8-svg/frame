-- ==========================================
-- Путевые заметки: структура базы данных
-- ==========================================

CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    country TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS travelers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER NOT NULL,
    traveler_id INTEGER NOT NULL,
    note_date TEXT NOT NULL,
    text TEXT NOT NULL DEFAULT '',
    is_archived INTEGER NOT NULL DEFAULT 0
        CHECK (is_archived IN (0, 1)),
    FOREIGN KEY (trip_id) REFERENCES trips(id),
    FOREIGN KEY (traveler_id) REFERENCES travelers(id)
);

-- Правило предметной области: на один день поездки
-- может быть только одна активная заметка.
CREATE UNIQUE INDEX IF NOT EXISTS ux_notes_active_day
ON notes (trip_id, note_date)
WHERE is_archived = 0;
