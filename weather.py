import requests
import pygame
import random
import math
import io

# OpenWeatherMap API Config
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_IMAGE_URL = "https://openweathermap.org/img/wn/"

# Function to fetch weather data
def get_weather(zip_code, country_code, api_key):
    """Fetch weather data from OpenWeatherMap based on zip code.

    Retrieves temperature, feels-like temperature, pressure, humidity, wind speed,
    wind direction, and weather reports from the OpenWeatherMap API.
    """
    try:
        print (f"Determining weather for {zip_code}...")
        url = f"{BASE_URL}?zip={zip_code},{country_code}&appid={api_key}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        feels_like = data["main"]["feels_like"]
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        wind_dir = _wind_direction(wind_deg, 16)
        reports = []
        for report in data["weather"]:
            weather = report["main"].lower()  # e.g., "clear", "clouds", "rain"
            image = report["icon"]
            image_url = f"{BASE_IMAGE_URL}{image}@2x.png"
            description = report["description"]
            reports.append({"weather": weather,
                            "description": description,
                            "image_url": image_url
                            })
            
        return temp, feels_like, pressure, humidity, wind_speed, wind_dir, reports
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None, None, None, None

def load_weather_icon(url):
    """Download the weather icon from OpenWeatherMap and return as a Pygame surface."""
    try:
        response = requests.get(url, timeout=5)  # Fetch the image
        response.raise_for_status()  # Raise error if request fails
        image = pygame.image.load(io.BytesIO(response.content))  # Convert to Pygame image
        return pygame.transform.scale(image, (100, 100))  # Resize if needed
    except requests.RequestException as e:
        print(f"Failed to load weather icon: {e}")
        return None
    
def _wind_direction(degrees, precision=8):
    """
    Converts wind direction in degrees (0-360) to a compass direction.
    
    :param degrees: Wind direction in degrees from OpenWeatherMap.
    :param precision: 8 for basic compass (N, NE, etc.), 16 for detailed (NNE, ENE, etc.).
    :return: Compass direction as a string.
    """
    compass_8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    compass_16 = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    
    if precision == 8:
        index = round(degrees / 45) % 8
        return compass_8[index]
    elif precision == 16:
        index = round(degrees / 22.5) % 16
        return compass_16[index]
    else:
        raise ValueError("Precision must be 8 or 16")
