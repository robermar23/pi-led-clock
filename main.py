import typer
import pygame
import datetime
import sys
import time
from util import setup_display, get_current_time, interpolate_color, get_config
from weather import get_weather, load_weather_icon
from background import get_background_color, draw_background_gradient, get_sun_times
from location import get_location


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

@app.command(
    context_settings={"ignore_unknown_options": True}
)
def start_clock(
  display: str = typer.Argument(":0", help="Display to run the show on (e.g., ':0')"),
  video_driver: str = typer.Argument("x11", help="Video driver to use (e.g., 'x11')"),
  screen_width: int = typer.Argument(800, help="Screen width (e.g., 800)"),
  screen_height: int = typer.Argument(480, help="Screen height (e.g., 480)"),
  utc_offset: int = typer.Argument(-5, help="UTC Offset for clock"),
  zip_code: str = typer.Argument("21047", help="Zipcode to determine weather for"),
  country_code: str = typer.Argument("us", help="Country code to determine weather for"),
  open_weather_api_key: str = typer.Argument("xxx", help="openweathermap.org api key")
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
    temp, feels_like, weather_reports = get_weather(zip_code, country_code, open_weather_api_key)
    if weather_reports:
        for report in weather_reports:
            report["weather_icon"] = load_weather_icon(report["image_url"])
            
    last_weather_update = time.time()  # Timestamp of the last weather update

    location = get_location()
    sun_rise, sun_set = get_sun_times(location)
    background_top_color = get_background_color(location, sun_rise, sun_set)
    background_bottom_color = interpolate_color(background_top_color, (0, 0, 0), 0.5)  # Darker shade

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        
        # Update weather data every hour
        current_time = time.time()
        if current_time - last_weather_update >= 3600:  # 3600 seconds = 1 hour
            temp, feels_like, weather_reports = get_weather(zip_code, country_code, open_weather_api_key)
            if weather_reports:
                for report in weather_reports:
                    report["weather_icon"] = load_weather_icon(report["image_url"])
    
            last_weather_update = current_time
            
            # Get gradient colors
            sun_rise, sun_set = get_sun_times(location)
            background_top_color = get_background_color(location, sun_rise, sun_set)
            background_bottom_color = interpolate_color(background_top_color, (0, 0, 0), 0.5)  # Darker shade

        draw_background_gradient(screen, screen_height, screen_width, background_top_color, background_bottom_color)

        # Get current time and date
        now = get_current_time(utc_offset)
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %B %d, %Y")

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
        
        if weather_reports:
            weather_report_base_x = 10
            weather_report_base_y = 10
            for report in weather_reports:
                screen.blit(report["weather_icon"], (weather_report_base_x, weather_report_base_y))
                weather_report_base_x = weather_report_base_y = (weather_report_base_x + 110)

         # Draw the moon only at night
        if now < sun_rise or now > sun_set:
            draw_moon(screen, timezone)

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

