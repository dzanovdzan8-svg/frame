from datetime import date

from django.conf import settings
from django.http import HttpResponse

from homepage.views import page
from models.notes import is_day_free
from models.trips import find_trip_by_id
from storage import load_notes, load_travelers, load_trips

TRIPS_FILE = settings.DATA_DIR / "trips.json"
TRAVELERS_FILE = settings.DATA_DIR / "travelers.json"
NOTES_FILE = settings.DATA_DIR / "notes.json"


def trips(request):
    items = ""
    for trip in load_trips(TRIPS_FILE):
        text = (
            f"{trip.title} ({trip.country}) – "
            f"{trip.duration_days} дн."
        )
        link = f'<a href="/trips/{trip.id}/">{text}</a>'
        items += f'<li class="list-group-item">{link}</li>'
    content = f"""
    <h1>Поездки</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Путевые заметки – поездки", content))


def trip_detail(request, trip_id):
    trips_list = load_trips(TRIPS_FILE)
    trip = find_trip_by_id(trips_list, trip_id)
    if trip is None:
        content = """
        <h1 class="text-danger">Поездка не найдена</h1>
        <a href="/trips/" class="btn btn-outline-secondary">
            ← к списку поездок
        </a>
        """
        return HttpResponse(
            page("Поездка не найдена", content),
            status=404,
        )
    travelers_list = load_travelers(TRAVELERS_FILE)
    notes_list = load_notes(NOTES_FILE, trips_list, travelers_list)
    today = date.today().isoformat()
    free = is_day_free(notes_list, trip, today)
    status = "заметки на сегодня нет" if free else "заметка на сегодня есть"
    badge = "bg-secondary" if free else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{trip.title}</h5>
            <p class="card-text"><strong>ID:</strong> {trip.id}</p>
            <p class="card-text">
                <strong>Страна:</strong> {trip.country}
            </p>
            <p class="card-text">
                <strong>Период:</strong>
                {trip.start_date} – {trip.end_date}
                ({trip.duration_days} дн.)
            </p>
            <p class="card-text">
                Заметка на текущую дату:
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/trips/" class="btn btn-outline-secondary">
                ← к списку поездок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(trip.title, content), status=200)
