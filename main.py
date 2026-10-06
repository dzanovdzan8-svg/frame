"""Начальный сценарий: проверка возможности добавить заметку к поездке."""
from datetime import date

trip_title = "Байкал: неделя на берегу"
country = "Россия"
start_date = date(2026, 7, 10)
end_date = date(2026, 7, 17)
budget = 56000.0
note_date = date(2026, 7, 12)
has_note = False


def count_trip_days(start, end):
    """Вернуть длительность поездки в днях (включая оба крайних дня)."""
    return (end - start).days + 1


def calc_daily_budget(total, days):
    """Вернуть средний бюджет на один день поездки."""
    if days <= 0:
        return 0.0
    return round(total / days, 2)


def is_day_in_trip(day, start, end):
    """Проверить, что день входит в период поездки."""
    return start <= day <= end


def get_note_status(day_in_trip, has_note_for_day):
    """Вернуть текстовый статус выбранного дня."""
    if not day_in_trip:
        return "Этот день не входит в период поездки"
    if has_note_for_day:
        return "На этот день заметка уже есть"
    return "Можно добавить заметку"


days = count_trip_days(start_date, end_date)
print(f"Поездка: {trip_title}")
print(f"Страна: {country}")
print(f"Период: {start_date} - {end_date}")
print(f"Длительность: {days} дн.")
print(f"Бюджет на день: {calc_daily_budget(budget, days)} руб.")
print(f"Выбранный день: {note_date}")
print(get_note_status(is_day_in_trip(note_date, start_date, end_date),
                      has_note))
