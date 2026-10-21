from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.trips, name="list"),
    path("available/", views.available_trips, name="available"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]
