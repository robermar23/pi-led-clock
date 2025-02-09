import pygame
import ephem
import datetime
import pytz

def get_moon_phase(timezone):
    """Calculate the current moon phase as a value between 0 (new moon) and 1 (full moon)."""
    now = datetime.datetime.now(pytz.timezone(timezone))
    moon_phase = ephem.Moon(now).phase  # Returns 0 to 29.53
    return moon_phase / 29.53  # Normalize to 0-1 scale
  
def draw_moon(surface, timezone):
    """Draw the moon with the correct phase."""
    moon_phase = get_moon_phase(timezone)  # Get phase as a value between 0 and 1

    width = surface.get_width()
    height = surface.get_height()
    
    # Moon settings
    moon_radius = min(width, height) // 8  # Scale moon size dynamically
    moon_x = width - moon_radius - 10  # Adjust to fit in the top-right corner
    moon_y = moon_radius + 10  # Adjust to fit in the top-right corner

    # Draw the full moon as a base
    pygame.draw.circle(surface, (200, 200, 200), (moon_x, moon_y), moon_radius)

    # Determine shadow position based on phase
    if moon_phase < 0.5:
        # Waxing phases: Shadow on the left
        shadow_x = MOON_X - int(moon_radius * (1 - 2 * moon_phase))
    else:
        # Waning phases: Shadow on the right
        shadow_x = MOON_X + int(moon_radius * (2 * moon_phase - 1))

    shadow_radius = MOON_RADIUS  # Keep the shadow the same size as the moon

    # Draw the shadow using a black circle to "cover" part of the moon
    pygame.draw.circle(surface, (0, 0, 0), (shadow_x, moon_y), shadow_radius)
