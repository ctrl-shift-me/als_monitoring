from django.shortcuts import render
from .utils import geocode_address, calculate_distance
from accounts.models import KioskOperatorProfile


def home(request):
    """Home page with search field"""
    context = {}
    search_location = ""

    if request.method == 'POST':
        search_location = request.POST.get('search_location', '')

    if search_location:
        search_location_geo = geocode_address(search_location)
        if search_location_geo:
            kiosk_operators = []
            providers = KioskOperatorProfile.objects.filter(
                # user type is kiosk operator
                # user_type=UserType.PROVIDER,
                is_available=True
            ).exclude(
                latitude__isnull=True
            ).exclude(
                longitude__isnull=True
            )

            # Can we make this more optimal?
            for operator in providers:
                if operator.latitude and operator.longitude:
                    distance = calculate_distance(
                        search_location_geo[0],
                        search_location_geo[1],
                        operator.latitude,
                        operator.longitude
                    )
                    kiosk_operators.append({
                        'operator': operator,
                        'distance': distance,
                    })
            # Sort by distance
            kiosk_operators.sort(key=lambda x: x['distance'])

            # Limit to 10 closest providers
            # optionally take in a variable to show n closest operators
            closest_operators = kiosk_operators[:5]

            context['search_provided'] = True
            context['search_location'] = search_location
            context['closest_operators'] = closest_operators
        else:
            context['geocoding_error'] = True

    return render(request, 'agent_finder/home.html', context)
