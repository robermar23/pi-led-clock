import geocoder
from astral import LocationInfo

def get_location():
    """Fetches the user's approximate location based on IP address."""
    g = geocoder.ip('me')  # Fetch geolocation data
    if g.latlng:
        lat, lon = g.latlng
        city = g.city or "Unknown"
        country = g.country or "Unknown"
        timezone = g.json.get("raw", {}).get("timezone", "UTC")
        return LocationInfo(city, country, timezone, lat, lon)
    else:
        return LocationInfo("Baltimore", "United States", "US/New York", 39.515362, -76.411751)  # Fallback
