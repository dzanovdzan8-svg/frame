from django.conf import settings
from django.shortcuts import render

from models.notes import find_note_by_id
from storage import load_notes, load_travelers, load_trips


def _load_notes():
    """Загрузить заметки со связями с поездками и авторами."""
    trips_list = load_trips(settings.DATA_DIR / "trips.json")
    travelers_list = load_travelers(settings.DATA_DIR / "travelers.json")
    return load_notes(
        settings.DATA_DIR / "notes.json",
        trips_list,
        travelers_list,
    )


def notes(request):
    context = {
        "notes": _load_notes(),
    }

    return render(
        request,
        "notes/note_list.html",
        context,
    )


def note_detail(request, note_id):
    note = find_note_by_id(_load_notes(), note_id)

    context = {
        "note": note,
    }

    return render(
        request,
        "notes/note_detail.html",
        context,
        status=404 if note is None else 200,
    )
