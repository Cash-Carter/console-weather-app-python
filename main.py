from dotenv import load_dotenv
import requests
from functools import partial
from datetime import datetime
import os

load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")

RESPONSE_LIMIT = "1"
GEOCODE_API_US_PARTIAL = partial(
    "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={RESPONSE_LIMIT}&appid={API_key}".format,
    RESPONSE_LIMIT=RESPONSE_LIMIT,
    API_key=OWM_API_KEY)
GEOCODE_API_PARTIAL = partial(
    "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit={RESPONSE_LIMIT}&appid={API_key}".format,
    RESPONSE_LIMIT=RESPONSE_LIMIT,
    API_key=OWM_API_KEY)
WEATHER_API_PARTIAL = partial(
    "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={units}".format,
    API_key=OWM_API_KEY)

US_CODES = {"US", "USA", "840"}
VALID_UNITS = {"standard", "metric", "imperial"}


def main():
    while True:
        name, lat, lon = ask_for_location()
        units = ask_for_units()

        print("requesting weather data...")
        response = requests.get(WEATHER_API_PARTIAL(lat=lat, lon=lon, units=units))
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            json = response.json()
            print(f"the weather in {name}:")
            print(f"the temprature is {temprature_format(units, json["main"]["temp"])}, feels like {temprature_format(units, json["main"]["feels_like"])}")
            print(f"the humidity is {json["main"]["humidity"]}%")
            print(f"wind speeds are {speed_format(units, json["wind"]["speed"])} blowing at {json["wind"]["deg"]}°")
            print(f"sunrise is at {time_format(json["sys"]["sunrise"])}")
            print(f"sunset is at {time_format(json["sys"]["sunset"])}")


def ask_for_location() -> (str, str, str):
    """returns (name, lat, lon)"""
    while True:
        country_code = input("input country (EX: US, USA, CA, CAN): ").strip().upper()
        """follows ISO 3166"""
        is_country_us = country_code in US_CODES

        if is_country_us:
            state_code = input("input state (EX: IL, VA): ").strip().upper()
        city_name = input("input city (EX: Chicago, Seattle): ").strip()

        if is_country_us:
            request = GEOCODE_API_US_PARTIAL(
                city_name=city_name,
                state_code=state_code,
                country_code=country_code)
        else:
            request = GEOCODE_API_PARTIAL(
                city_name=city_name,
                country_code=country_code)

        print("requesting location data...")
        response = requests.get(request)
        try:
            response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            if json := response.json():
                json = json[0]
                return json["name"], json["lat"], json["lon"]
        print("no location found, try again")


def ask_for_units() -> str:
    while True:
        units = input("input units (standard, metric, imperial): ").strip().lower()
        if units in VALID_UNITS:
            return units
        print("invalid units, try again")


def temprature_format(units, temprature):
    match units:
        case "standard":
            return f"{temprature}K"
        case "metric":
            return f"{temprature}°C"
        case "imperial":
            return f"{temprature}°F"


def speed_format(units, temprature):
    match units:
        case "standard" | "metric":
            return f"{temprature}m/s"
        case "imperial":
            return f"{temprature}mph"


def time_format(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%H:%M:%S")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nbye bye")
