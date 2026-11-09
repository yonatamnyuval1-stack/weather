import json
from urllib.request import urlopen
from urllib.parse import quote

def find_city(city_name):
    safe_name = quote(city_name)
    url = "https://geocoding-api.open-meteo.com/v1/search?name=" + safe_name + "&count=1"
    try:
        with urlopen(url) as response:
            data = json.load(response)
    except Exception:
        print("could not reach the city.")
        return None
    results = data.get("results")
    if not results:
        print("City not found.")
        return None
    return results[0] 

def describe_weather_code(code):
    names = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Cloudy",
        45: "Fog",
        48: "Fog",
        51: "light drizzle",
        53: "drizzle",
        55: "heavy drizzle",
        61: "light rain",
        63: "rain",
        65: "heavy rain",
        71: "light snow",
        73: "snow",
        75: "heavy snow",
        80: "rain showers",
        81: "rain showers",
        82: "heavy rain showers",
        95: "thunderstorm",
        96: "thunderstorm",
        99: "thunderstorm",
    }
    if code in names:
        return names[code]
    return "Unknown"

def get_live_weather(city_name):
    place = find_city(city_name)
    if place is None:
        return None
    latitude = place["latitude"]
    longitude = place["longitude"]
    url = (
        "https://api.open-meteo.com/v1/forecast"
        + "?latitude=" + str(latitude)
        + "&longitude=" + str(longitude)
        + "&current=temperature_2m,relative_humidity_2m,weather_code"
    )
    try:
        with urlopen(url) as response:
            data = json.load(response)
    except Exception:
        print("could not get the weather.")
        return None
    current = data["current"]
    weather = {
        "city": place["name"],
        "temperature": round(current["temperature_2m"]),
        "humidity": current["relative_humidity_2m"],
        "condition": describe_weather_code(current["weather_code"]),
    }
    return weather