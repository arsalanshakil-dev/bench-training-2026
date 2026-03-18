import requests
import os
from datetime import datetime, timedelta, timezone

api_key = os.getenv("WEATHER_API_KEY")
city = "Lahore"

r = requests.get(
    "https://api.openweathermap.org/data/2.5/weather",
    params={"q": city, "appid": api_key},
)

if r.status_code == 200:
    data = r.json()
    print(f"Raw data: {data}")

    coord = data["coord"]

    r2 = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"lat": coord["lat"], "lon": coord["lon"], "appid": api_key, "units": "metric"},
    )

    if r2.status_code == 200:
        forecast = r2.json()
        print(f"Raw forecast data: {forecast}")
        print("\nFormatted forecast data:")
        print(f"City: {forecast['name']}")
        print(f"Temperature: {forecast['main']['temp']} °C")
        print(f"Wind speed: {forecast['wind']['speed']} m/s")
        print(f"Weather description: {forecast['weather'][0]['description']}")
