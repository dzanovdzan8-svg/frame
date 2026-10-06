from django.test import TestCase, override_settings


class HomepageTests(TestCase):
    def test_index_uses_templates(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")

    def test_index_title_and_links(self):
        response = self.client.get("/")
        self.assertContains(response, "Главная – Путевые заметки")
        self.assertContains(response, 'href="/trips/"')
        self.assertContains(response, 'href="/notes/"')

    def test_static_files_are_linked(self):
        response = self.client.get("/")
        self.assertContains(response, "/static/homepage/css/style.css")
        self.assertContains(response, "/static/homepage/js/main.js")
        self.assertContains(response, "/static/homepage/img/logo.png")

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(
            response, "страница не найдена", status_code=404
        )
