from django.urls import path, include
from .views import enrolment_form_view, create_custom_form_view, custom_form_success_view

urlpatterns = [
    path("enrol/", enrolment_form_view, name="enrolment_form"),
    path("schools/<int:school_id>/custom-form/create/", create_custom_form_view, name="create_custom_form"),
    path("custom-form/success/", custom_form_success_view, name="custom_form_success"),

    path("accounts/", include("django.contrib.auth.urls")),
]