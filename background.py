import pygame
import datetime
import pytz
import random
from astral import LocationInfo
from astral.sun import sun
from colorsys import rgb_to_hsv, hsv_to_rgb
from util import interpolate_color
from cloud import Cloud
from star import Star

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

    print (f"Current time: {now}, Sunrise: {sunrise}, Sunset: {sunset}, Dawn start: {dawn_start}, Dusk end: {dusk_end}")
    
    if now < dawn_start:
        # Deep night
        print("Deep night")
        return color_night
    elif dawn_start <= now < sunrise:
        # Dawn transition
        print("Dawn transition")
        factor = (now - dawn_start).total_seconds() / (sunrise - dawn_start).total_seconds()
        return interpolate_color(color_night, color_dawn, factor)
    elif sunrise <= now < (sunrise + datetime.timedelta(minutes=30)):
        # Morning transition
        print("Morning transition")
        factor = (now - sunrise).total_seconds() / (30 * 60)
        return interpolate_color(color_dawn, color_day, factor)
    elif (sunrise + datetime.timedelta(minutes=30)) <= now < (sunset - datetime.timedelta(minutes=30)):
        # Daytime
        print("Daytime")
        return color_day
    elif (sunset - datetime.timedelta(minutes=30)) <= now < sunset:
        # Pre-sunset transition
        print("Pre-sunset transition")
        factor = (now - (sunset - datetime.timedelta(minutes=30))).total_seconds() / (30 * 60)
        return interpolate_color(color_day, color_sunset, factor)
    elif sunset <= now < dusk_end:
        # Sunset to night transition
        print("Sunset to night transition")
        factor = (now - sunset).total_seconds() / (dusk_end - sunset).total_seconds()
        return interpolate_color(color_sunset, color_night, factor)
    else:
        # Night
        print("Night")
        return color_night


def draw_background_gradient(surface, screen_height, screen_width, top_color, bottom_color):
    """Draw a vertical gradient from top_color to bottom_color."""
    for y in range(screen_height):
        factor = y / screen_height
        color = interpolate_color(top_color, bottom_color, factor)
        pygame.draw.line(surface, color, (0, y), (screen_width, y))

# def draw_starry_sky(screen, width, height, star_count=100):
#     #screen.fill((10, 10, 30))  # dark night blue
#     for _ in range(star_count):
#         x = random.randint(0, width)
#         y = random.randint(0, height)
#         radius = random.choice([1, 2])
#         color = random.choice([(255, 255, 255), (255, 255, 200)])  # white to pale yellow
#         pygame.draw.circle(screen, color, (x, y), radius)

# def draw_cloudy_night(screen, width, height):
#     #base_color = (20, 20, 40)  # darker bluish-grey
#     #screen.fill(base_color)
#     cloud_surface = pygame.Surface((width, height), pygame.SRCALPHA)

#     for _ in range(8):  # number of clouds
#         x = random.randint(0, width)
#         y = random.randint(0, height // 2)  # top half only
#         w = random.randint(100, 250)
#         h = random.randint(40, 100)
#         alpha = random.randint(30, 70)
#         color = (100, 100, 120, alpha)  # soft grey with alpha
#         pygame.draw.ellipse(cloud_surface, color, (x, y, w, h))

    #screen.blit(cloud_surface, (0, 0))

def draw_cloudy_night(screen, width, height, clouds):
    #screen.fill((20, 20, 40))  # base night color
    cloud_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for cloud in clouds:
        cloud.update(width)
        cloud.draw(cloud_surface)

    screen.blit(cloud_surface, (0, 0))

def draw_starry_sky(screen, width, height, stars):
    #screen.fill((10, 10, 30))  # deep night sky
    for star in stars:
        star.update()
        star.draw(screen)
