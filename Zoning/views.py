import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from shapely.geometry import Point, shape

from .models import SchoolZone


def zone_checker_page(request):
    return render(request, "zoning/zone_checker.html", {
        "mapbox_token": settings.MAPBOX_ACCESS_TOKEN,
    })


@require_GET
def search_schools(request):
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"results": []})

    schools = (
        SchoolZone.objects
        .filter(poly_name__istartswith=query)
        .only("id", "poly_name")
        .order_by("poly_name")[:10]
    )

    results = [
        {
            "id": school.id,
            "name": school.poly_name
        }
        for school in schools
    ]

    return JsonResponse({"results": results})

@require_POST
def check_zone(request):
    try:
        data = json.loads(request.body)

        school_id = data.get("school_id")
        lng = data.get("lng")
        lat = data.get("lat")

        if not school_id:
            return JsonResponse({
                "success": False,
                "message": "Please select a school."
            }, status=400)

        if lng is None or lat is None:
            return JsonResponse({
                "success": False,
                "message": "Please select an address from the suggestions."
            }, status=400)

        school_zone = get_object_or_404(SchoolZone, id=school_id)

        if not school_zone.geojson_boundary:
            return JsonResponse({
                "success": False,
                "message": "This school does not have zone geometry saved."
            }, status=400)

        polygon = shape(school_zone.geojson_boundary)
        point = Point(float(lng), float(lat))

        inside = polygon.contains(point) or polygon.touches(point)

        return JsonResponse({
            "success": True,
            "school": school_zone.poly_name,
            "inside_zone": inside,
            "message": (
                f"This address is inside {school_zone.poly_name}'s zone."
                if inside else
                f"This address is outside {school_zone.poly_name}'s zone."
            )
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Error: {str(e)}"
        }, status=500)