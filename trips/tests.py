import sqlite3

from django.test import TestCase

from db.testing import use_test_database


class TripPagesTests(TestCase):
    def setUp(self):
        self.db_path = use_test_database(self)

    def test_trip_list_uses_templates_and_data(self):
        response = self.client.get("/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/trip_list.html")
        self.assertTemplateUsed(response, "trips/includes/trip_card.html")
        self.assertContains(response, "Всего поездок: 3")
        self.assertContains(response, 'href="/trips/1/"')

    def test_trip_list_reads_database_not_json(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE trips SET title = 'Новое имя' WHERE id = 1")
        conn.commit()
        conn.close()
        response = self.client.get("/trips/")
        self.assertContains(response, "Новое имя")
        self.assertNotContains(response, "Байкал")

    def test_filter_by_country(self):
        response = self.client.get("/trips/", {"country": "Турция"})
        self.assertContains(response, "Всего поездок: 1")
        self.assertContains(response, "Стамбул")

    def test_filter_by_min_days(self):
        response = self.client.get("/trips/", {"min_days": 9})
        self.assertContains(response, "Всего поездок: 1")
        self.assertContains(response, "Золотое кольцо")

    def test_filter_without_results(self):
        response = self.client.get("/trips/", {"country": "Нигерия"})
        self.assertContains(response, "Поездки не найдены.")

    def test_wrong_min_days_is_ignored(self):
        response = self.client.get("/trips/", {"min_days": "abc"})
        self.assertContains(response, "Всего поездок: 3")

    def test_trip_detail_with_notes(self):
        response = self.client.get("/trips/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/trip_detail.html")
        self.assertContains(response, "Заметки поездки (3)")
        self.assertContains(response, "Анна Смирнова")

    def test_missing_trip_returns_404(self):
        response = self.client.get("/trips/9999/")
        self.assertContains(
            response, "Поездка не найдена", status_code=404
        )

    def test_available_page_without_date(self):
        response = self.client.get("/trips/available/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/available.html")

    def test_available_trip_on_free_day(self):
        response = self.client.get(
            "/trips/available/", {"date": "2026-07-15"}
        )
        self.assertContains(response, "Байкал")

    def test_busy_day_is_not_available(self):
        response = self.client.get(
            "/trips/available/", {"date": "2026-07-12"}
        )
        self.assertNotContains(response, "Байкал")
        self.assertContains(response, "нет поездок")

    def test_archived_note_frees_the_day(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("UPDATE notes SET is_archived = 1 WHERE id = 1")
        conn.commit()
        conn.close()
        response = self.client.get(
            "/trips/available/", {"date": "2026-07-12"}
        )
        self.assertContains(response, "Байкал")

    def test_invalid_date_and_sql_injection_are_safe(self):
        for value in ("не дата", "2026-07-12' OR '1'='1"):
            response = self.client.get(
                "/trips/available/", {"date": value}
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Неверный формат даты.")
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
        conn.close()
        self.assertEqual(count, 3)


class EmptyTripsTests(TestCase):
    def test_empty_database_does_not_break_pages(self):
        use_test_database(self, with_data=False)
        response = self.client.get("/trips/")
        self.assertContains(response, "Поездки не найдены.")
        response = self.client.get("/trips/1/")
        self.assertEqual(response.status_code, 404)
