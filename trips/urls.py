from django.urls import path

from . import views

app_name = "trips"

urlpatterns = [
    path("", views.trips, name="list"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]
