from django.test import TestCase


class NotePagesTests(TestCase):
    def test_note_list(self):
        response = self.client.get("/notes/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Байкал")

    def test_note_detail(self):
        response = self.client.get("/notes/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Анна Смирнова")

    def test_missing_note_returns_404(self):
        response = self.client.get("/notes/9999/")
        self.assertContains(
            response, "Заметка не найдена", status_code=404
        )
