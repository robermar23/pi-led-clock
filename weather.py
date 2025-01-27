import requests
import pygame
import random

# OpenWeatherMap API Config
API_KEY = "0abddaaa4a4c778e6200331ca19de26d"  # Replace with your API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def get_weather(zip_code, country_code):
    try:
        url = f"{BASE_URL}?zip={zip_code},{country_code}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather = data["weather"][0]["main"].lower()  # e.g., "clear", "clouds", "rain"
        return temp, weather, feels_like
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None

# Function to determine background color or graphics based on weather
def get_weather_background(screen, weather, screen_size, frame_count):
    """
    Draws the weather graphics in the top-right corner of the screen.
    """
    screen_width, screen_height = screen_size
    corner_position = (screen_width - 150, 50)

    if weather == "clear":
        screen.fill((135, 206, 235))  # Light blue for sunny
        draw_sun(screen, corner_position)
    elif weather in ["clouds", "overcast"]:
        screen.fill((169, 169, 169))  # Gray for cloudy
        draw_clouds(screen, corner_position)
    elif weather == "rain":
        screen.fill((100, 149, 237))  # Steel blue for rain
        draw_rain(screen, corner_position, frame_count)
    else:
        screen.fill((25, 25, 112))  # Midnight blue for unknown weather

# Functions to draw weather graphics
def draw_sun(screen, position):
    """
    Draws a sun with rays at the specified position.
    """
    center_x, center_y = position
    radius = 50
    ray_length = 20
    ray_color = (255, 223, 0)  # Yellow
    num_rays = 12

    # Draw the central circle for the sun
    pygame.draw.circle(screen, (255, 223, 0), (center_x, center_y), radius)

    # Draw the rays
    for i in range(num_rays):
        angle = (360 / num_rays) * i
        start_x = center_x + int(radius * 1.2 * pygame.math.cos(pygame.math.radians(angle)))
        start_y = center_y - int(radius * 1.2 * pygame.math.sin(pygame.math.radians(angle)))
        end_x = center_x + int((radius + ray_length) * pygame.math.cos(pygame.math.radians(angle)))
        end_y = center_y - int((radius + ray_length) * pygame.math.sin(pygame.math.radians(angle)))
        pygame.draw.line(screen, ray_color, (start_x, start_y), (end_x, end_y), 3)

def draw_clouds(screen, position):
    """
    Draws realistic fluffy clouds at the specified position.
    """
    x, y = position
    cloud_color = (211, 211, 211)  # Light gray for clouds

    # Draw base ellipses for the cloud
    base_shapes = [
        (x, y, 100, 60),
        (x + 50, y - 30, 120, 80),
        (x + 90, y + 10, 90, 50),
        (x - 20, y + 20, 80, 40),
    ]
    for shape in base_shapes:
        pygame.draw.ellipse(screen, cloud_color, shape)

    # Add a slight shadow effect
    shadow_color = (169, 169, 169)  # Darker gray
    pygame.draw.ellipse(screen, shadow_color, (x + 40, y + 40, 100, 40))


def draw_rain(screen, position, frame_count):
    """
    Draws animated rain at the specified position.
    """
    x, y = position
    rain_color = (135, 206, 250)  # Light blue for rain
    rain_drops = []

    # Generate raindrop positions
    for i in range(30):  # 30 raindrops
        drop_x = x + random.randint(-100, 100)
        drop_y = y + random.randint(-50, 50) + (frame_count % 30) * 5  # Animated vertical movement
        drop_length = random.randint(10, 20)
        rain_drops.append((drop_x, drop_y, drop_x + 2, drop_y + drop_length))

    # Draw raindrops
    for drop in rain_drops:
        pygame.draw.line(screen, rain_color, (drop[0], drop[1]), (drop[2], drop[3]), 2)
