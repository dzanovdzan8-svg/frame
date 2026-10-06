from django.test import TestCase, override_settings


class HomepageTests(TestCase):
    def test_index_opens(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Путевые заметки")

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response, "страница не найдена", status_code=404
        )
