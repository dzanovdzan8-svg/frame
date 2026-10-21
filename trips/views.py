import sqlite3
from contextlib import closing
from datetime import date

from django.shortcuts import render

from db.database import get_connection


def trips(request):
    country = request.GET.get("country", "")
    try:
        min_days = int(request.GET.get("min_days", 1))
    except ValueError:
        min_days = 1

    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        trips_data = conn.execute(
            """
            SELECT * FROM (
                SELECT
                    id,
                    title,
                    country,
                    start_date,
                    end_date,
                    CAST(julianday(end_date) - julianday(start_date)
                         AS INTEGER) + 1 AS duration_days
                FROM trips
            )
            WHERE (? = '' OR country = ?)
              AND duration_days >= ?
            ORDER BY start_date;
            """,
            [country, country, min_days],
        ).fetchall()
        countries = conn.execute(
            "SELECT DISTINCT country FROM trips ORDER BY country;"
        ).fetchall()

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips_data,
            "countries": countries,
            "selected_country": country,
            "min_days": min_days,
        },
    )


def trip_detail(request, trip_id):
    with closing(get_connection()) as conn:
        conn.row_factory = sqlite3.Row
        trip = conn.execute(
            """
            SELECT
                id,
                title,
                country,
                start_date,
                end_date,
                CAST(julianday(end_date) - julianday(start_date)
                     AS INTEGER) + 1 AS duration_days
            FROM trips
            WHERE id = ?;
            """,
            [trip_id],
        ).fetchone()

        context = {"trip": trip}

        if trip is not None:
            context["trip_notes"] = conn.execute(
                """
                SELECT
                    notes.id,
                    notes.note_date,
                    notes.text,
                    notes.is_archived,
                    travelers.name AS traveler_name
                FROM notes
                JOIN travelers
                    ON notes.traveler_id = travelers.id
                WHERE notes.trip_id = ?
                ORDER BY notes.note_date;
                """,
                [trip_id],
            ).fetchall()
            today_notes = conn.execute(
                """
                SELECT COUNT(*) AS notes_count
                FROM notes
                WHERE trip_id = ?
                  AND note_date = ?
                  AND is_archived = 0;
                """,
                [trip_id, date.today().isoformat()],
            ).fetchone()
            context["today_free"] = today_notes["notes_count"] == 0

    return render(
        request,
        "trips/trip_detail.html",
        context,
        status=404 if trip is None else 200,
    )


def available_trips(request):
    note_date = request.GET.get("date", "")
    trips_data = []
    error = ""

    if note_date:
        try:
            date.fromisoformat(note_date)
        except ValueError:
            error = "Неверный формат даты."
        else:
            with closing(get_connection()) as conn:
                conn.row_factory = sqlite3.Row
                trips_data = conn.execute(
                    """
                    SELECT
                        trips.id,
                        trips.title,
                        trips.country
                    FROM trips
                    WHERE ? BETWEEN trips.start_date AND trips.end_date
                      AND trips.id NOT IN (
                          SELECT notes.trip_id
                          FROM notes
                          WHERE notes.note_date = ?
                            AND notes.is_archived = 0
                      )
                    ORDER BY trips.title;
                    """,
                    [note_date, note_date],
                ).fetchall()

    return render(
        request,
        "trips/available.html",
        {
            "trips": trips_data,
            "note_date": note_date,
            "error": error,
        },
    )
