# pi-led-clock

Python based clock and weather app, designed to render on LED's on a Raspberry PI

I built this as a project for leaning the basics of pygame when and interacting with a screen embedded on an RaspBerry PI.

## Dependencies

- OpenWeatherMap api key, see `https://openweathermap.org/` for a free key for retrieving current weather metrics.  The app will make an api call once an hour.
- Screen to display the weather clock on.  It is expected that whatever you are running this app on has a GUI that is capable of rendering pygame graphics. 
  - if on linux, it will use x11 as the display driver
  - if on windows, it will use an sdlc compatible driver, directx.  
  - This is a simple 2d graphics app so should work with most display drivers

## Install

This app uses poetry for package management

```sh
poetry install
```

## Run

For displaying all parameters and their meaning:

```sh
poetry run main.py --help
```

```sh
python main.py --help
```

### Example

#### Linux

Render on the default 800x480 led screen, showing weather and time for America/New_York timezone

```sh
poetry run main.py -- ':0' 'x11' 800 480 'America/New_York' '20001' 'us' 'YOUR-OPENWEATHERMAP-API-KEY'
```

#### Windows

Render on the second display, in a 700x400 box at the top left of the screen, showing weather and time for Australia Fair, Queensland

```sh
python main.py -- '1' 'directx' 700 400 'Australia/Brisbane' '4215' 'au' 'YOUR-OPENWEATHERMAP-API-KEY'
```
