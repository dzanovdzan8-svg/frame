import sqlite3
from contextlib import closing

from django.shortcuts import render

from db.database import get_connection

STATUSES = {
    "active": ("Активные", 0),
    "archived": ("Архивные", 1),
    "all": ("Все", 0),
}


def notes(request):
    status = request.GET.get("status", "active")
    if status not in STATUSES:
        status = "active"

    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        notes_data = conn.execute(
            """
            SELECT
                notes.id,
                notes.note_date,
                notes.text,
                notes.is_archived,
                trips.title AS trip_title,
                travelers.name AS traveler_name
            FROM notes
            JOIN trips
                ON notes.trip_id = trips.id
            JOIN travelers
                ON notes.traveler_id = travelers.id
            WHERE (? = 'all' OR notes.is_archived = ?)
            ORDER BY notes.note_date, notes.id;
            """,
            [status, STATUSES[status][1]],
        ).fetchall()

    return render(
        request,
        "notes/note_list.html",
        {
            "notes": notes_data,
            "status": status,
            "statuses": STATUSES,
        },
    )


def note_detail(request, note_id):
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        note = conn.execute(
            """
            SELECT
                notes.id,
                notes.note_date,
                notes.text,
                notes.is_archived,
                trips.id AS trip_id,
                trips.title AS trip_title,
                travelers.name AS traveler_name
            FROM notes
            JOIN trips
                ON notes.trip_id = trips.id
            JOIN travelers
                ON notes.traveler_id = travelers.id
            WHERE notes.id = ?;
            """,
            [note_id],
        ).fetchone()

    return render(
        request,
        "notes/note_detail.html",
        {"note": note},
        status=404 if note is None else 200,
    )


def statistics(request):
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        summary = conn.execute(
            """
            SELECT
                COUNT(*) AS trips_count,
                CAST(MIN(julianday(end_date) - julianday(start_date))
                     AS INTEGER) + 1 AS min_days,
                CAST(MAX(julianday(end_date) - julianday(start_date))
                     AS INTEGER) + 1 AS max_days,
                ROUND(AVG(julianday(end_date) - julianday(start_date) + 1),
                      1) AS avg_days
            FROM trips;
            """
        ).fetchone()
        notes_count = conn.execute(
            """
            SELECT COUNT(*) AS notes_count
            FROM notes
            WHERE is_archived = 0;
            """
        ).fetchone()
        trip_stats = conn.execute(
            """
            SELECT
                trips.title AS trip_title,
                COUNT(notes.id) AS notes_count
            FROM trips
            LEFT JOIN notes
                ON trips.id = notes.trip_id
                AND notes.is_archived = 0
            GROUP BY trips.id, trips.title
            ORDER BY notes_count DESC, trips.title;
            """
        ).fetchall()
        traveler_stats = conn.execute(
            """
            SELECT
                travelers.name AS traveler_name,
                COUNT(notes.id) AS notes_count
            FROM travelers
            LEFT JOIN notes
                ON travelers.id = notes.traveler_id
                AND notes.is_archived = 0
            GROUP BY travelers.id, travelers.name
            ORDER BY notes_count DESC, travelers.name;
            """
        ).fetchall()
        country_stats = conn.execute(
            """
            SELECT
                country,
                COUNT(*) AS trips_count,
                SUM(CAST(julianday(end_date) - julianday(start_date)
                         AS INTEGER) + 1) AS total_days
            FROM trips
            GROUP BY country
            ORDER BY trips_count DESC, country;
            """
        ).fetchall()
        busy_trips = conn.execute(
            """
            SELECT
                trips.title AS trip_title,
                COUNT(notes.id) AS notes_count
            FROM trips
            JOIN notes
                ON trips.id = notes.trip_id
            WHERE notes.is_archived = 0
            GROUP BY trips.id, trips.title
            HAVING COUNT(notes.id) > 1
            ORDER BY notes_count DESC;
            """
        ).fetchall()
        latest_notes = conn.execute(
            """
            SELECT
                notes.id,
                notes.note_date,
                trips.title AS trip_title
            FROM notes
            JOIN trips
                ON notes.trip_id = trips.id
            WHERE notes.is_archived = 0
            ORDER BY notes.note_date DESC
            LIMIT 3;
            """
        ).fetchall()

    return render(
        request,
        "notes/statistics.html",
        {
            "summary": summary,
            "notes_count": notes_count["notes_count"],
            "trip_stats": trip_stats,
            "traveler_stats": traveler_stats,
            "country_stats": country_stats,
            "busy_trips": busy_trips,
            "latest_notes": latest_notes,
        },
    )
