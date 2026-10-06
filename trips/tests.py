import json
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings


class TripPagesTests(TestCase):
    def test_trip_list_uses_templates_and_filter_length(self):
        response = self.client.get("/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/trip_list.html")
        self.assertTemplateUsed(response, "trips/includes/trip_card.html")
        self.assertContains(response, "Всего поездок: 3")
        self.assertContains(response, 'href="/trips/1/"')

    def test_trip_detail(self):
        response = self.client.get("/trips/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/trip_detail.html")
        self.assertContains(response, "Байкал")
        self.assertContains(response, "Заметки поездки (1)")

    def test_missing_trip_returns_404(self):
        response = self.client.get("/trips/9999/")
        self.assertContains(
            response, "Поездка не найдена", status_code=404
        )

    def test_empty_trip_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "trips.json").write_text("[]", encoding="utf-8")
            with override_settings(DATA_DIR=Path(tmp)):
                response = self.client.get("/trips/")
        self.assertContains(response, "Поездки не найдены.")
        self.assertContains(response, "Всего поездок: 0")

    def test_default_filter_for_empty_title(self):
        data = [{"id": 1, "title": "", "country": "Россия",
                 "start_date": "2026-07-10", "end_date": "2026-07-12"}]
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "trips.json").write_text(
                json.dumps(data), encoding="utf-8"
            )
            with override_settings(DATA_DIR=Path(tmp)):
                response = self.client.get("/trips/")
        self.assertContains(response, "Без названия")
