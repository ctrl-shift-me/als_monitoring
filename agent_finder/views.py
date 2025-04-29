from django.shortcuts import render
from .utils import geocode_address, calculate_distance
from accounts.models import KioskOperatorProfile, SuperAgentProfile


def home(request):
    """Home page with search field"""
    context = {}
    search_location = ""
    user_type = "all"  # Default to showing all types

    if request.method == 'POST':
        search_location = request.POST.get('search_location', '')
        user_type = request.POST.get('user_type', 'all')

    if search_location:
        search_location_geo = geocode_address(search_location)
        if search_location_geo:
            # kiosk_operators = []
            results = []

            # Get profiles based on the user_type filter
            # providers_query = KioskOperatorProfile.objects.filter(
            #     is_available=True)
            if user_type == "KO":
                kiosk_operators = KioskOperatorProfile.objects.filter(
                    is_available=True
                ).exclude(
                    latitude__isnull=True
                ).exclude(
                    longitude__isnull=True
                )

                for operator in kiosk_operators:
                    if operator.latitude and operator.longitude:
                        distance = calculate_distance(
                            search_location_geo[0],
                            search_location_geo[1],
                            operator.latitude,
                            operator.longitude
                        )
                        results.append({
                            'operator': operator,
                            'distance': distance,
                            'type': 'KO'
                        })

            if user_type == "SA":
                # super_agents = SuperAgentProfile.objects.exclude(
                #     latitude__isnull=True
                # ).exclude(
                #     longitude__isnull=True
                # )
                super_agents = SuperAgentProfile.objects.all()

                for agent in super_agents:
                    # if agent.latitude and agent.longitude:
                    #     distance = calculate_distance(
                    #         search_location_geo[0],
                    #         search_location_geo[1],
                    #         agent.latitude,
                    #         agent.longitude
                    #     )
                    #     results.append({
                    #         'operator': agent,
                    #         'distance': distance,
                    #         'type': 'SA'
                    #     })
                    results.append({
                        'operator': agent,
                        'distance': 'N/A',
                        'type': 'SA '
                    })

            # Sort by distance
            # kiosk_operators.sort(key=lambda x: x['distance'])
            results.sort(key=lambda x: x['distance'])

            # Limit to 10 closest providers
            # optionally take in a variable to show n closest operators
            # closest_operators = kiosk_operators[:5]
            closest_operators = results[:5]

            context['search_provided'] = True
            context['search_location'] = search_location
            context['closest_operators'] = closest_operators
            context['user_type'] = user_type
        else:
            context['geocoding_error'] = True
            context['user_type'] = user_type

    return render(request, 'agent_finder/home.html', context)
