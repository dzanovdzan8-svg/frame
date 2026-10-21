from django.test import TestCase

from db.testing import use_test_database


class NotePagesTests(TestCase):
    def setUp(self):
        use_test_database(self)

    def test_active_notes_by_default(self):
        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertTemplateUsed(response, "notes/includes/note_status.html")
        self.assertContains(response, "Всего заметок: 6")
        self.assertNotContains(response, "Черновик")

    def test_all_and_archived_filters(self):
        response = self.client.get("/notes/", {"status": "all"})
        self.assertContains(response, "Всего заметок: 7")
        response = self.client.get("/notes/", {"status": "archived"})
        self.assertContains(response, "Всего заметок: 1")
        self.assertContains(response, "В архиве")

    def test_unknown_status_falls_back_to_active(self):
        response = self.client.get("/notes/", {"status": "'; DROP"})
        self.assertContains(response, "Всего заметок: 6")

    def test_note_detail_joins_trip_and_author(self):
        response = self.client.get("/notes/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_detail.html")
        self.assertContains(response, "Анна Смирнова")
        self.assertContains(response, "Байкал")
        self.assertContains(response, "Активна")

    def test_missing_note_returns_404(self):
        response = self.client.get("/notes/9999/")
        self.assertContains(
            response, "Заметка не найдена", status_code=404
        )

    def test_statistics_page(self):
        response = self.client.get("/notes/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/statistics.html")
        self.assertContains(response, "Активных заметок: 6")
        self.assertContains(response, "в среднем 6,7 дн.")
        self.assertContains(response, "Россия: поездок 2")
        self.assertContains(response, "Байкал: неделя на берегу – 3")

    def test_statistics_includes_trip_without_notes_count(self):
        response = self.client.get("/notes/statistics/")
        self.assertContains(response, "Стамбул за выходные")


class EmptyNotesTests(TestCase):
    def test_empty_database_does_not_break_pages(self):
        use_test_database(self, with_data=False)
        response = self.client.get("/notes/")
        self.assertContains(response, "Заметки не найдены.")
        response = self.client.get("/notes/statistics/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Таких поездок пока нет.")
