import sys
from weather_lib import get_live_weather, is_raining, is_snowing, hottest_city, coldest_city

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
        line = weather["city"] + ": " + str(weather["temperature"]) + " degrees " + weather["condition"]
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

def show_snow(city_name):
    weather = get_live_weather(city_name)
    if weather is None:
        return
    if is_snowing(weather):
        print("Yes, it is snowing in " + weather["city"])
    else:
        print("No, it is not snowing in " + weather["city"])

def show_coldest(city_names):
    weather_list = []
    for city_name in city_names:
        weather = get_live_weather(city_name)
        if weather is None:
            return
        weather_list.append(weather)
    name = coldest_city(weather_list)
    print(name + "is the coldest.")

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
    elif command == "snow":
        show_snow(cities[0])
    elif command == "coldest":
        show_coldest(cities)
    else:
        print("unknown command")