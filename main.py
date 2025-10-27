from dotenv import load_dotenv
import requests
import os

load_dotenv()

appid = os.getenv("OWM_API_KEY")
location = "Chicago"
units = "imperial"

print(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={appid}&units={units}")

#response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={appid}")

#response.json()