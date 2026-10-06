import json
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings


class NotePagesTests(TestCase):
    def test_note_list_uses_templates(self):
        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertTemplateUsed(response, "notes/includes/note_status.html")
        self.assertContains(response, "Всего заметок: 2")
        self.assertContains(response, 'href="/notes/1/"')

    def test_note_detail(self):
        response = self.client.get("/notes/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_detail.html")
        self.assertContains(response, "Анна Смирнова")
        self.assertContains(response, "Активна")

    def test_missing_note_returns_404(self):
        response = self.client.get("/notes/9999/")
        self.assertContains(
            response, "Заметка не найдена", status_code=404
        )

    def test_empty_note_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "notes.json").write_text("[]", encoding="utf-8")
            with override_settings(DATA_DIR=Path(tmp)):
                response = self.client.get("/notes/")
        self.assertContains(response, "Заметки не найдены.")

    def test_archived_note_status(self):
        trips = [{"id": 1, "title": "Байкал", "country": "Россия",
                  "start_date": "2026-07-10", "end_date": "2026-07-17"}]
        travelers = [{"id": 1, "name": "Анна", "email": "a@example.com"}]
        notes = [{"id": 1, "trip_id": 1, "note_date": "2026-07-12",
                  "traveler_id": 1, "text": "Строка 1\nСтрока 2",
                  "is_archived": True}]
        files = {"trips": trips, "travelers": travelers, "notes": notes}
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in files.items():
                Path(tmp, f"{name}.json").write_text(
                    json.dumps(data), encoding="utf-8"
                )
            with override_settings(DATA_DIR=Path(tmp)):
                response = self.client.get("/notes/1/")
        self.assertContains(response, "В архиве")
        self.assertContains(response, "Строка 1<br>Строка 2")
