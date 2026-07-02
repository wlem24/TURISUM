import math

SAUDI_LAT_MIN, SAUDI_LAT_MAX = 16.0, 32.5
SAUDI_LNG_MIN, SAUDI_LNG_MAX = 34.5, 56.0


def is_within_saudi_arabia(lat: float, lng: float) -> bool:
    return (SAUDI_LAT_MIN <= lat <= SAUDI_LAT_MAX) and (SAUDI_LNG_MIN <= lng <= SAUDI_LNG_MAX)


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def bounding_box(lat: float, lng: float, radius_km: float) -> tuple[float, float, float, float]:
    """Return (min_lat, max_lat, min_lng, max_lng) for a bounding box."""
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (math.cos(math.radians(lat)) * 111.0 + 1e-10)
    return lat - lat_delta, lat + lat_delta, lng - lng_delta, lng + lng_delta
