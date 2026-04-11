from django.urls import path
from .views import enrolment_form_view

urlpatterns = [
    path("enrol/", enrolment_form_view, name="enrolment_form"),
]