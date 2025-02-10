import pygame
import ephem
import datetime
import pytz

def get_moon_phase(timezone):
    """Calculate the current moon phase as a value between 0 (new moon) and 1 (full moon)."""
    now = datetime.datetime.now(pytz.timezone(timezone))
    moon_phase = ephem.Moon(now).phase  # Returns 0 to 29.53
    return moon_phase / 29.53  # Normalize to 0-1 scale
    #return moon_phase % 10

def draw_moon(surface, timezone):
    """Draw the moon with the correct phase."""
    moon_phase = get_moon_phase(timezone)  # Get phase as a value between 0 and 1

    width = surface.get_width()
    height = surface.get_height()

    # Moon settings
    radius = min(width, height) // 25  # Scale moon size dynamically
    x = width - radius - 10  # Adjust to fit in the top-right corner
    y = radius + 20  # Adjust to fit in the top-right corner

    # Colors
    moon_color = (230, 230, 230)
    shadow_color = (10, 10, 10)

    # Draw full moon base
    pygame.draw.circle(surface, moon_color, (x, y), radius)

    moon_phase = int(moon_phase)  # Convert to integer for switch statement

    # Overlay shadow based on phase
    if moon_phase == 0:  # New Moon
        pygame.draw.circle(surface, shadow_color, (x, y), radius)
    elif moon_phase == 1:  # Waxing Crescent
        pygame.draw.rect(surface, shadow_color, (x - radius, y - radius, radius, radius * 2))
    elif moon_phase == 2:  # First Quarter
        pygame.draw.rect(surface, shadow_color, (x, y - radius, radius, radius * 2))
    elif moon_phase == 3:  # Waxing Gibbous
        pygame.draw.ellipse(surface, shadow_color, (x, y - radius, radius, radius * 2))
    elif moon_phase == 4:  # Full Moon (nothing to draw)
        pass
    elif moon_phase == 5:  # Waning Gibbous
        pygame.draw.ellipse(surface, shadow_color, (x - radius, y - radius, radius, radius * 2))
    elif moon_phase == 6:  # Third Quarter
        pygame.draw.rect(surface, shadow_color, (x - radius, y - radius, radius, radius * 2))
    elif moon_phase == 7:  # Waning Crescent
        pygame.draw.rect(surface, shadow_color, (x, y - radius, radius, radius * 2))
