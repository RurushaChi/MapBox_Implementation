from django.urls import path
from .views import zone_check_view

urlpatterns = [
    path("schools/<int:school_id>/zone-check/", zone_check_view, name="zone_check"),
]