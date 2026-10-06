from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from models.notes import find_note_by_id
from storage import load_notes, load_travelers, load_trips

TRIPS_FILE = settings.DATA_DIR / "trips.json"
TRAVELERS_FILE = settings.DATA_DIR / "travelers.json"
NOTES_FILE = settings.DATA_DIR / "notes.json"


def _load_all():
    trips_list = load_trips(TRIPS_FILE)
    travelers_list = load_travelers(TRAVELERS_FILE)
    return load_notes(NOTES_FILE, trips_list, travelers_list)


def notes(request):
    items = ""
    for note in _load_all():
        status = "в архиве" if note.is_archived else "активна"
        badge = "bg-secondary" if note.is_archived else "bg-success"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/notes/{note.id}/">
                {note.trip.title} – {note.note_date}
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Заметки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Путевые заметки – заметки", content))


def note_detail(request, note_id):
    note = find_note_by_id(_load_all(), note_id)
    if note is None:
        content = """
        <h1 class="text-danger">Заметка не найдена</h1>
        <a href="/notes/" class="btn btn-outline-secondary">
            ← к списку заметок
        </a>
        """
        return HttpResponse(
            page("Заметка не найдена", content),
            status=404,
        )
    status = "в архиве" if note.is_archived else "активна"
    badge = "bg-secondary" if note.is_archived else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заметка №{note.id}</h5>
            <p class="card-text">Поездка: {note.trip.title}</p>
            <p class="card-text">Дата: {note.note_date}</p>
            <p class="card-text">Автор: {note.traveler.name}</p>
            <p class="card-text">{note.text}</p>
            <p class="card-text">
                Статус: <span class="badge {badge}">{status}</span>
            </p>
            <a href="/notes/" class="btn btn-outline-secondary">
                ← к списку заметок
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Заметка №{note.id}", content),
        status=200,
    )
