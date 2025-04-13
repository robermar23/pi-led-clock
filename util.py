import os
import sys
import pygame
import json
import pytz
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

# Constants
BLACK = (0, 0, 0)

def get_current_time(utc_offset: int):
    """Get the current time with a specified UTC offset.

    Calculates the current time adjusted for the given UTC offset.
    """
    offset = timezone(timedelta(hours=utc_offset))
    now = datetime.now(offset)
    return now

def get_current_time(timezone_name: str):
    tz = pytz.timezone(timezone_name)
    now = datetime.now(tz)
    return now

def setup_display(display: str, video_driver: str, screen_width: int, screen_height: int):
    """
    Set up the display environment and initialize pygame.
    """
    os.putenv("DISPLAY", display)
    os.putenv("SDL_VIDEODRIVER", video_driver)

    pygame.init()

    # Detect platform
    platform = sys.platform
    print(f"Running on platform: {platform}")
    if platform.startswith("linux"):
        print("Running on Linux, using framebuffer")
        pygame.display.init()
        size = (screen_width, screen_height)
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        pygame.font.init()
        pygame.display.update()

    elif platform.startswith("win"):
        print("Running on Windows, using sdl2")
        os.putenv("SDL_VIDEODRIVER", "")
        pygame.display.init()
        # Get screen resolution of the selected display
        display_info = pygame.display.Info()
        display_index = int(display)
            # Position the window manually to support 2 displays atm
        if display_index == 1:  # Second monitor
            #print(f"Display info: {display_info}")
            width = display_info.current_w
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{width},0"  # Place at the start of the second screen
        else:  # Primary monitor
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        screen.fill(BLACK)
        pygame.font.init()
        pygame.display.update()

    #this screen object is what is used to create everything else
    return screen 

def interpolate_color(color1, color2, factor):
    """Linearly interpolate between two colors."""
    return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))

def get_config(file_path = "config.json"):
    """Loads a JSON file and returns an object with dynamic attributes."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))

# Function to draw glowing text
def draw_text(surface, text, font, color, position, glow_color, glow_radius):
    """Draw text with a glow effect on a surface.

    Renders the given text with a specified glow, by blurring the text using
    multiple blits with an offset.
    """
    
    glow_surface = font.render(text, True, glow_color)
    for offset in range(1, glow_radius + 1):
        glow_pos = (position[0] - offset, position[1] - offset)
        surface.blit(glow_surface, glow_pos)
    # Render the main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)