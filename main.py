import json
import sys
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

def is_raining(weather):
    condition = weather["condition"].lower()
    wet_words = ["rain", "drizzle", "shower", "thunderstorm"]
    for word in wet_words:
        if word in condition:
            return True
    return False

def hottest_city(weather_list):
    if not weather_list:
        return None
    hottest = weather_list[0]
    for weather in weather_list:
        if weather["temperature"] > hottest["temperature"]:
            hottest = weather
    return hottest["city"]

def coldest_city(weather_list):
    if not weather_list:
        return None
    coldest = weather_list[0]
    for weather in weather_list:
        if weather["temperature"] < coldest["temperature"]:
            coldest = weather
    return coldest["city"]

def show_temp(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return
    print(str(weather["temperature"]) + " degrees")

def show_humidity(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return
    print("humidity: " + str(weather["humidity"]))

def show_condition(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return
    print(weather["condition"])

def show_compare(city_names):
    for city_name in city_names:
        weather = get_live_weather(city_name)
        if weather is None:
            return
        line = weather["city"] + ": " + str(weather["temperature "]) + "degrees " + weather["condition"]
        print(line)

def show_now(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return

    print("city:", weather["city"])
    print("temperature: " + str(weather["temperature"]))
    print("humidity: " + str(weather["humidity"]))
    print("condition:", weather["condition"])

def show_rain(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return
    if is_raining(weather):
        print("Yes, it is raining in " + weather["city"])
    else:
        print("No, it is not raining in " + weather["city"])

def show_hottest(city_names):
    weather_list = []
    for city_name in city_names:
        weather = get_live_weather(city_name)
        if weather is None:
            return
        weather_list.append(weather)
    name = hottest_city(weather_list)
    print(name + "is the hottest.")
if len(sys.argv) < 3:
    print("try: python main.py now <city_name>")
else:
    command = sys.argv[1]
    cities = sys.argv[2:]
    if command == "now":
        show_now(cities[0])
    elif command == "rain":
        show_rain(cities[0])
    elif command == "hottest":
        show_hottest(cities)
    elif command == "compare":
        show_compare(cities)
    elif command == "temp":
        show_temp(cities[0])
    elif command == "humidity":
        show_humidity(cities[0])
    elif command == "condition":
        show_condition(cities[0])
    else:
        print("unknown command")