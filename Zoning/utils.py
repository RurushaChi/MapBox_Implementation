from shapely.geometry import Point, shape
from .models import SchoolZone


def find_school_zone(lat, lng):
    point = Point(lng, lat)  # IMPORTANT: (lng, lat)

    zones = SchoolZone.objects.all()

    for zone in zones:
        geometry = zone.geojson_boundary

        if not geometry:
            continue

        polygon = shape(geometry)

        if polygon.contains(point):
            return {
                "school": zone.poly_name,
                "zone_id": zone.poly_id
            }

    return None