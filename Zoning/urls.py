from django.urls import path
from .views import zone_checker_page, search_schools, check_zone

urlpatterns = [
    path("checker/", zone_checker_page, name="zone_checker_page"),
    path("search-schools/", search_schools, name="search_schools"),
    path("check-zone/", check_zone, name="check_zone"),
]