"""Маршрутизация верхнего уровня проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("trips/", include("trips.urls")),
    path("notes/", include("notes.urls")),
]

handler404 = "homepage.views.page_not_found"
