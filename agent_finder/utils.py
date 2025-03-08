from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def geocode_address(address):
    geolocator = Nominatim(user_agent="finder_app")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except:
        pass
    return None


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers
