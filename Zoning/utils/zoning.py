import requests
from shapely.geometry import shape, Point


def geocode_address(address):
    """
    Convert an address into latitude and longitude using Nominatim.
    """

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "nz"
    }
    headers = {
        "User-Agent": "EduEnrol/1.0 (student project)"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    results = response.json()

    if not results:
        return None

    first_result = results[0]

    return {
        "latitude": float(first_result["lat"]),
        "longitude": float(first_result["lon"]),
        "display_name": first_result.get("display_name", address)
    }


def check_if_point_in_zone(zone_geojson, longitude, latitude):
    """
    Check whether a longitude/latitude point is inside the zone polygon.
    """

    if zone_geojson.get("type") == "Feature":
        geometry_data = zone_geojson["geometry"]
    else:
        geometry_data = zone_geojson

    polygon = shape(geometry_data)
    point = Point(longitude, latitude)

    return polygon.covers(point)