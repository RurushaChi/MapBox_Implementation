import json
from datetime import datetime
from django.core.management.base import BaseCommand
from Zoning.models import SchoolZone


class Command(BaseCommand):
    help = "Import school zones from a GeoJSON file"

    def add_arguments(self, parser):
        parser.add_argument("geojson_file", type=str)

    def handle(self, *args, **options):
        file_path = options["geojson_file"]

        self.stdout.write("Starting import...")
        self.stdout.write(f"Opening file: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            self.stdout.write("Reading JSON file...")
            data = json.load(f)

        self.stdout.write("JSON loaded successfully.")

        features = data.get("features", [])
        self.stdout.write(f"Found {len(features)} features.")

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for i, feature in enumerate(features, start=1):
            self.stdout.write(f"Processing feature {i}...")

            try:
                properties = feature.get("properties", {})
                geometry = feature.get("geometry")

                if not properties or not geometry:
                    skipped_count += 1
                    continue

                school_id = properties.get("SchoolID")
                poly_id = properties.get("PolyID")
                poly_name = properties.get("PolyName")
                office = properties.get("Office")
                approval_date = properties.get("ApprovalDate")
                effective_date = properties.get("EffectiveDate")
                inst_type = properties.get("INSTTYPE")

                if poly_id is None:
                    skipped_count += 1
                    continue

                if approval_date:
                    approval_date = datetime.strptime(approval_date, "%Y-%m-%d").date()
                else:
                    approval_date = None

                if effective_date:
                    effective_date = datetime.strptime(effective_date, "%Y-%m-%d").date()
                else:
                    effective_date = None

                obj, created = SchoolZone.objects.update_or_create(
                    poly_id=poly_id,
                    defaults={
                        "school_id_from_file": school_id,
                        "poly_name": poly_name,
                        "office": office,
                        "approval_date": approval_date,
                        "effective_date": effective_date,
                        "inst_type": inst_type,
                        "geojson_boundary": geometry,
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"Skipped feature {i}: {e}"))

        self.stdout.write(self.style.SUCCESS("Import complete"))
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped: {skipped_count}")