from django.contrib import admin
from .models import School, SchoolZone


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "ministry_id"]
    search_fields = ["name", "ministry_id"]


@admin.register(SchoolZone)
class SchoolZoneAdmin(admin.ModelAdmin):
    list_display = ["id", "poly_name", "school_id_from_file", "poly_id", "office"]
    search_fields = ["poly_name", "school_id_from_file", "poly_id"]