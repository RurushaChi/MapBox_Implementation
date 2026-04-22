from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Enrolment_Form.urls')),  # 👈 ADD THIS
    path('', include('Zoning.urls')),
]