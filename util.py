import os
import sys
import pygame
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Constants
BLACK = (0, 0, 0)

def get_current_time(utc_offset: int):
  offset = timezone(timedelta(hours=utc_offset))
  now = datetime.now(offset)
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
        screen.fill(BLACK)
        pygame.font.init()
        pygame.display.update()
    elif platform.startswith("win"):
        print("Running on Windows, using sdl2")
        os.putenv("SDL_VIDEODRIVER", "")
        pygame.display.init()
        # Get screen resolution of the selected display
        display_info = pygame.display.Info()
        #print(f"Display info: {display_info}")
        width = display_info.current_w
        display_index = int(display)
        # Position the window manually to support 2 displays atm
        if display_index == 1:  # Second monitor
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{width},0"  # Place at the start of the second screen
        else:  # Primary monitor
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

        screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
        screen.fill(BLACK)
        pygame.font.init()
        pygame.display.update()

    #this screen object is what is used to create everything else
    return screen 