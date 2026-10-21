from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.notes, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:note_id>/", views.note_detail, name="detail"),
]
