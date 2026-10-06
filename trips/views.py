from datetime import date

from django.conf import settings
from django.shortcuts import render

from models.notes import is_day_free
from models.trips import find_trip_by_id
from storage import load_notes, load_travelers, load_trips


def trips(request):
    trips_list = load_trips(settings.DATA_DIR / "trips.json")

    context = {
        "trips": trips_list,
    }

    return render(
        request,
        "trips/trip_list.html",
        context,
    )


def trip_detail(request, trip_id):
    trips_list = load_trips(settings.DATA_DIR / "trips.json")
    trip = find_trip_by_id(trips_list, trip_id)

    context = {"trip": trip}

    if trip is not None:
        travelers_list = load_travelers(
            settings.DATA_DIR / "travelers.json"
        )
        notes_list = load_notes(
            settings.DATA_DIR / "notes.json",
            trips_list,
            travelers_list,
        )
        context["trip_notes"] = [
            note for note in notes_list if note.trip.id == trip.id
        ]
        context["today_free"] = is_day_free(
            notes_list,
            trip,
            date.today().isoformat(),
        )

    return render(
        request,
        "trips/trip_detail.html",
        context,
        status=404 if trip is None else 200,
    )
