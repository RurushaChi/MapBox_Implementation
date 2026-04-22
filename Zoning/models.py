from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255)
    ministry_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name




class SchoolZone(models.Model):
    school_id_from_file = models.IntegerField(blank=True, null=True)
    poly_id = models.BigIntegerField(unique=True, blank=True, null=True)
    poly_name = models.CharField(max_length=255, blank=True, null=True)
    office = models.CharField(max_length=10, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    inst_type = models.CharField(max_length=100, blank=True, null=True)
    geojson_boundary = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.poly_name or f"Zone {self.id}"