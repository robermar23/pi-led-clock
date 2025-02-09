import pygame
import datetime
import pytz
from astral import LocationInfo
from astral.sun import sun
from colorsys import rgb_to_hsv, hsv_to_rgb
from util import interpolate_color

def get_sun_times(location):
    """Retrieve sunrise and sunset times for the current day."""
    now = datetime.datetime.now(pytz.timezone(location.timezone))
    s = sun(location.observer, date=now.date(), tzinfo=location.timezone)
    return s["sunrise"].astimezone(pytz.timezone(location.timezone)), s["sunset"].astimezone(pytz.timezone(location.timezone))

def get_background_color(location, sunrise, sunset):
    """Determine background color based on the time of day."""
    now = datetime.datetime.now(pytz.timezone(location.timezone))
    
    print (f"location: {location.timezone}")
    print (f"sunrise: {sunrise}, sunset: {sunset}")

    # Define key colors
    color_night = (10, 10, 40)        # Deep blue
    color_dawn = (255, 120, 70)       # Orange-pink
    color_day = (135, 206, 250)       # Bright blue
    color_sunset = (255, 90, 40)      # Deep orange-red
    color_twilight = (25, 25, 112)    # Dark blue

    # Calculate position in the day cycle
    if now < sunrise:
        factor = (now - (sunrise - datetime.timedelta(hours=1))).total_seconds() / 3600
        return interpolate_color(color_night,color_dawn, max(0, min(1, factor)))
    elif sunrise <= now < sunset:
        factor = (now - sunrise).total_seconds() / (sunset - sunrise).total_seconds()
        return interpolate_color(color_day, color_dawn, max(0, min(1, factor)))
    else:
        factor = (now - sunset).total_seconds() / 3600
        return interpolate_color(color_sunset, color_night, max(0, min(1, factor)))

def draw_background_gradient(surface, screen_height, screen_width, top_color, bottom_color):
    """Draw a vertical gradient from top_color to bottom_color."""
    for y in range(screen_height):
        factor = y / screen_height
        color = interpolate_color(top_color, bottom_color, factor)
        pygame.draw.line(surface, color, (0, y), (screen_width, y))

