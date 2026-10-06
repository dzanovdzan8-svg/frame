from django.urls import path

from . import views

urlpatterns = [
    path("", views.notes, name="notes"),
    path("<int:note_id>/", views.note_detail, name="note_detail"),
]
