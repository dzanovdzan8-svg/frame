from django.test import TestCase


class TripPagesTests(TestCase):
    def test_trip_list(self):
        response = self.client.get("/trips/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Байкал")

    def test_trip_detail(self):
        response = self.client.get("/trips/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Байкал")

    def test_missing_trip_returns_404(self):
        response = self.client.get("/trips/9999/")
        self.assertContains(
            response, "Поездка не найдена", status_code=404
        )
