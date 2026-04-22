from django.shortcuts import render, get_object_or_404
from .models import School, SchoolZone
from .forms import AddressZoneCheckForm
from .utils.zoning import geocode_address, check_if_point_in_zone



def zone_check_view(request, school_id):
    school = get_object_or_404(School, id=school_id)
    zone = get_object_or_404(SchoolZone, school=school, is_active=True)

    result = None
    error_message = None

    if request.method == "POST":
        form = AddressZoneCheckForm(request.POST)

        if form.is_valid():
            address = form.cleaned_data["address"]

            geocode_result = geocode_address(address)

            if not geocode_result:
                error_message = "Address could not be found."
            else:
                latitude = geocode_result["latitude"]
                longitude = geocode_result["longitude"]

                in_zone = check_if_point_in_zone(
                    zone.geojson_boundary,
                    longitude,
                    latitude
                )

                if in_zone:
                    zoning_status = "In zone"
                else:
                    zoning_status = "Out of zone"

                result = {
                    "school_name": school.name,
                    "address": address,
                    "matched_address": geocode_result["display_name"],
                    "latitude": latitude,
                    "longitude": longitude,
                    "zoning_status": zoning_status
                }
    else:
        form = AddressZoneCheckForm()

    return render(request, "zone_check.html", {
        "school": school,
        "form": form,
        "result": result,
        "error_message": error_message
    })


from django.shortcuts import render

# Create your views here.
