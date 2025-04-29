import typer
import pygame
import sys
import time
import random
from util import setup_display, get_current_time, interpolate_color, get_config, draw_text
from weather import get_weather, load_weather_icon
from background import get_background_color, draw_background_gradient, get_sun_times, draw_starry_sky, draw_cloudy_night
from location import get_location
from moon import draw_moon
from cloud import Cloud
from star import Star
from raindrop import Raindrop

app = typer.Typer()

@app.command(
    context_settings={"ignore_unknown_options": True}
)
def start_clock(
    display: str = typer.Argument(":0", help="Display to run the show on (e.g., ':0')"),
    video_driver: str = typer.Argument("x11", help="Video driver to use (e.g., 'x11')"),
    screen_width: int = typer.Argument(800, help="Screen width (e.g., 800)"),
    screen_height: int = typer.Argument(480, help="Screen height (e.g., 480)"),
    timezone_name: str = typer.Argument("UTC", help="Timezone for the clock"),
    zip_code: str = typer.Argument("xxxxx", help="Zipcode to determine weather for"),
    country_code: str = typer.Argument("us", help="Country code to determine weather for"),
    open_weather_api_key: str = typer.Argument("xxx", help="openweathermap.org api key"),

):
    """
    Start the clock
    """
    
    # Set up the screen
    screen = setup_display(display, video_driver, screen_width, screen_height)
    pygame.display.set_caption("Dynamic Clock")

    # Load fonts
    clock_font, date_font, weather_font, weather_det_font = _load_fonts(screen_height)

    running = True
    clock = pygame.time.Clock()
    frame_count = 0

    # Fetch initial weather data
    weather_data = _update_weather(zip_code, country_code, open_weather_api_key)
    last_weather_update = time.time()  # Timestamp of the last weather update

    location = get_location()
    sun_rise, sun_set = get_sun_times(location)
    background_colors = _get_background_colors(location, sun_rise, sun_set)
    
    clouds = create_clouds(screen_width, screen_height)
    stars = create_stars(screen_width, screen_height)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen
        
        # Update weather data every hour
        current_time = time.time()
        if current_time - last_weather_update >= 3600:  # 3600 seconds = 1 hour
            weather_data = _update_weather(zip_code, country_code, open_weather_api_key)
            last_weather_update = current_time
            sun_rise, sun_set = get_sun_times(location)
            background_colors = _get_background_colors(location,  sun_rise, sun_set)
            
        draw_background_gradient(screen, screen_height, screen_width, *background_colors)

        # Get current time and date
        now = get_current_time(timezone_name)
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        
        # Increment frame count for animation
        frame_count += 1

        # Calculate text positions
        text_positions = _calculate_text_positions(screen, now, weather_data, clock_font, date_font, weather_font, weather_det_font)

        _draw_weather_icons(screen, weather_data)
        
        if now < sun_rise or now > sun_set:
            _draw_night_effects(screen, screen_width, screen_height, weather_data[6][0]["weather"], clouds, stars)
        
        # Draw the moon only at night
        if now < sun_rise or now > sun_set:
            draw_moon(screen, location.timezone)

        # Draw time and date with glow
        draw_text(screen, time_str, clock_font, (255, 255, 255), text_positions["clock"], (0, 0, 0), 3)
        draw_text(screen, date_str, date_font, (255, 255, 255), text_positions["date"], (0, 0, 0), 2)
        draw_text(screen, text_positions["weather_text"], weather_font, (255, 255, 255), text_positions["weather"], (0, 0, 0), 2)
        draw_text(screen, text_positions["weather_det_text"], weather_det_font, (255, 255, 255), text_positions["weather_det"], (0, 0, 0), 2)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

def _draw_night_effects(screen, width, height, weather_condition, clouds, stars):
    if weather_condition in ["clear", "clear sky"]:
        draw_starry_sky(screen, width, height, stars)
    elif weather_condition in ["clouds", "overcast clouds", "broken clouds"]:
        draw_cloudy_night(screen, width, height, clouds)
    


def _load_fonts(screen_height):
    """Load fonts with sizes relative to the screen height.

    Initializes Pygame fonts and creates font objects for clock, date, and weather
    information, with sizes dynamically scaled based on screen height.
    """
    pygame.font.init()
    clock_font_size = int(screen_height * 0.3)
    date_font_size = int(screen_height * 0.1)
    weather_font_size = int(screen_height * 0.1)
    weather_det_font_size = int(screen_height * 0.04)
    clock_font = pygame.font.Font(pygame.font.match_font("arial"), clock_font_size)
    date_font = pygame.font.Font(pygame.font.match_font("arial"), date_font_size)
    weather_font = pygame.font.Font(pygame.font.match_font("arial"), weather_font_size)
    weather_det_font = pygame.font.Font(pygame.font.match_font("arial"), weather_det_font_size)
    return clock_font, date_font, weather_font, weather_det_font

def _update_weather(zip_code, country_code, open_weather_api_key):
    """Update weather data from OpenWeatherMap.

    Fetches weather information using the provided API key and location details,
    and loads associated weather icons.
    """
    temp, feels_like, pressure, humidity, wind_speed, wind_deg, weather_reports = get_weather(zip_code, country_code, open_weather_api_key)
    if weather_reports:
        for report in weather_reports:
            report["weather_icon"] = load_weather_icon(report["image_url"])
    return temp, feels_like, pressure, humidity, wind_speed, wind_deg, weather_reports

def _get_background_colors(location, sun_rise, sun_set):
    """Calculate background gradient colors based on sun times.

    Determines the top and bottom colors for the background gradient using the
    location and sunrise/sunset times, making the bottom color a darker shade.
    """
    background_top_color = get_background_color(location, sun_rise, sun_set)
    background_bottom_color = interpolate_color(background_top_color, (0, 0, 0), 0.5)
    
    print(f"Background Top Color: {background_top_color}, Bottom Color: {background_bottom_color}")
    
    return background_top_color, background_bottom_color


def _calculate_text_positions(screen, now, weather_data, clock_font, date_font, weather_font, weather_det_font):
    """Calculate the positions for displaying text elements on the screen.

    Determines the screen positions for the clock, date, and weather information,
    centering them horizontally and positioning them vertically with appropriate
    spacing.
    """
    screen_width, screen_height = screen.get_size()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %B %d, %Y")
    temp, feels_like, pressure, humidity, wind_speed, wind_deg, _ = weather_data
    weather_text = f"{temp:.1f}°F, feels like {feels_like}°F" if temp is not None else "Weather Unavailable"
    weather_det_text = f"Humidity: {humidity}, Pressure: {pressure}, Wind {wind_speed} {wind_deg}"

    clock_text_width, clock_text_height = clock_font.size(time_str)
    date_text_width, date_text_height = date_font.size(date_str)
    weather_text_width, weather_text_height = weather_font.size(weather_text)
    weather_det_text_width, weather_det_text_height = weather_det_font.size(weather_det_text)

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
    weather_det_position = (
        (screen_width - weather_det_text_width) // 2,
        weather_position[1] + weather_text_height + 20
    )

    return {
        "clock": clock_position,
        "date": date_position,
        "weather": weather_position,
        "weather_det": weather_det_position,
        "weather_text": weather_text,
        "weather_det_text": weather_det_text,
    }


def _draw_weather_icons(screen, weather_data):
    """Draw weather icons on the screen.

    Blits weather icons onto the screen based on the weather data, positioning
    them horizontally with a fixed offset.
    """
    _, _, _, _, _, _, weather_reports = weather_data
    if weather_reports:
        weather_report_base_x = 10
        weather_report_base_y = 10
        for report in weather_reports:
            screen.blit(report["weather_icon"], (weather_report_base_x, weather_report_base_y))
            weather_report_base_x = weather_report_base_y = (weather_report_base_x + 110)
            

def create_clouds(width, height, count=8):
    clouds = []
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height // 2)
        w = random.randint(100, 250)
        h = random.randint(40, 100)
        alpha = random.randint(30, 70)
        speed_x = random.uniform(0.03, 0.12)  # very slow drift
        clouds.append(Cloud(x, y, w, h, alpha, speed_x))
    return clouds

def create_stars(width, height, count=100):
    stars = []
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.choice([1, 2])
        color = random.choice([(255, 255, 255), (255, 255, 200)])
        stars.append(Star(x, y, radius, color))
    return stars

def create_raindrops(width, height, count=75):
    raindrops = []
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(-height, 0)
        length = random.randint(5, 15)
        speed = random.uniform(2, 5)
        raindrops.append(Raindrop(x, y, length, speed))
    return raindrops



if __name__ == "__main__":
    app()

