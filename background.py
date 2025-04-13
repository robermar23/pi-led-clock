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
    now = datetime.datetime.now(pytz.timezone(location.timezone))

    # Define key colors
    color_night = (10, 10, 40)
    color_dawn = (255, 120, 70)
    color_day = (135, 206, 250)
    color_sunset = (255, 90, 40)
    color_twilight = (25, 25, 112)

    dawn_start = sunrise - datetime.timedelta(minutes=45)
    dusk_end = sunset + datetime.timedelta(minutes=45)

    if now < dawn_start:
        # Deep night
        return color_night
    elif dawn_start <= now < sunrise:
        # Dawn transition
        factor = (now - dawn_start).total_seconds() / (sunrise - dawn_start).total_seconds()
        return interpolate_color(color_night, color_dawn, factor)
    elif sunrise <= now < (sunrise + datetime.timedelta(minutes=30)):
        # Morning transition
        factor = (now - sunrise).total_seconds() / (30 * 60)
        return interpolate_color(color_dawn, color_day, factor)
    elif (sunrise + datetime.timedelta(minutes=30)) <= now < (sunset - datetime.timedelta(minutes=30)):
        # Daytime
        return color_day
    elif (sunset - datetime.timedelta(minutes=30)) <= now < sunset:
        # Pre-sunset transition
        factor = (now - (sunset - datetime.timedelta(minutes=30))).total_seconds() / (30 * 60)
        return interpolate_color(color_day, color_sunset, factor)
    elif sunset <= now < dusk_end:
        # Sunset to night transition
        factor = (now - sunset).total_seconds() / (dusk_end - sunset).total_seconds()
        return interpolate_color(color_sunset, color_night, factor)
    else:
        # Night
        return color_night


def draw_background_gradient(surface, screen_height, screen_width, top_color, bottom_color):
    """Draw a vertical gradient from top_color to bottom_color."""
    for y in range(screen_height):
        factor = y / screen_height
        color = interpolate_color(top_color, bottom_color, factor)
        pygame.draw.line(surface, color, (0, y), (screen_width, y))

