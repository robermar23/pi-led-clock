import typer
import pygame
import datetime
import sys
from util import setup_display, get_current_time
from weather import get_weather, get_weather_background

app = typer.Typer()

# Function to draw glowing text
def draw_text(surface, text, font, color, position, glow_color, glow_radius):
    # Create the glow effect by blurring the text
    glow_surface = font.render(text, True, glow_color)
    for offset in range(1, glow_radius + 1):
        glow_pos = (position[0] - offset, position[1] - offset)
        surface.blit(glow_surface, glow_pos)
    # Render the main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)
    
@app.command()
def start_clock(
  display: str = typer.Argument(":0", help="Display to run the show on (e.g., ':0')"),
  video_driver: str = typer.Argument("x11", help="Video driver to use (e.g., 'x11')"),
  screen_width: int = typer.Argument(800, help="Screen width (e.g., 800)"),
  screen_height: int = typer.Argument(480, help="Screen height (e.g., 480)"),
  utc_offset: int = typer.Argument(-5, help="UTC Offset for clock"),
  zip_code: str = typer.Argument("21047", help="Zipcode to determine weather for"),
  country_code: str = typer.Argument("us", help="Country code to determine weather for")
):
    """
    Start the clock
    """
    
     # Set up the screen
    screen = setup_display(display, video_driver, screen_width, screen_height)
    pygame.display.set_caption("Dynamic Clock")

    # Load fonts
    pygame.font.init()
    clock_font_size = int(screen_height * 0.3)  # Dynamic font size for the clock
    date_font_size = int(screen_height * 0.1)  # Smaller font size for the date
    weather_font_size = int(screen_height * 0.1)  # Font size for weather info
    clock_font = pygame.font.Font(pygame.font.match_font("arial"), clock_font_size)
    date_font = pygame.font.Font(pygame.font.match_font("arial"), date_font_size)
    weather_font = pygame.font.Font(pygame.font.match_font("arial"), weather_font_size)

    running = True
    clock = pygame.time.Clock()
    frame_count = 0

    # Fetch initial weather data
    temp, weather, feels_like = get_weather(zip_code, country_code)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get current time and date
        now = get_current_time(utc_offset)
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %B %d, %Y")

        # Update background color based on time
        # background_color = get_background_color(now.hour)
        # screen.fill(background_color)

         # Update the background based on the weather
         # Update the background with weather graphics
        get_weather_background(screen, weather, (screen_width, screen_height), frame_count)

        # Increment frame count for animation
        frame_count += 1

        # Calculate text positions
        clock_text_width, clock_text_height = clock_font.size(current_time)
        date_text_width, date_text_height = date_font.size(current_date)
        weather_text = f"{temp:.1f}°F, feels like {feels_like}°F" if temp is not None else "Weather Unavailable"
        weather_text_width, weather_text_height = weather_font.size(weather_text)

        clock_position = (
            (screen_width - clock_text_width) // 2,
            (screen_height - clock_text_height) // 3,
        )
        date_position = (
            (screen_width - date_text_width) // 2,
            clock_position[1] + clock_text_height + 20,
        )
        weather_position = (
            (screen_width - weather_text_width) // 2,
            date_position[1] + date_text_height + 20,
        )

        # Draw time and date with glow
        draw_text(screen,current_time,clock_font,(255, 255, 255),clock_position,(0, 0, 0),3)

        draw_text(screen,current_date,date_font,(255, 255, 255),date_position,(0, 0, 0), 2)

        draw_text(screen, weather_text, weather_font, (255, 255, 255), weather_position, (0, 0, 0), 2)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    app()

