# weather_fetcher.py

import requests
import pandas as pd
from datetime import datetime

# ── 1. Define the cities you want weather for ──────────────────
cities = {
    "Bengaluru": {"latitude": 12.97, "longitude": 77.59},
    "Mumbai":    {"latitude": 19.07, "longitude": 72.87},
    "Delhi":     {"latitude": 28.61, "longitude": 77.20},
    "Chennai":   {"latitude": 13.08, "longitude": 80.27},
    "Hyderabad": {"latitude": 17.38, "longitude": 78.48},
}

# ── 2. Fetch weather for each city ─────────────────────────────
all_weather = []

for city, coords in cities.items():
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude":         coords["latitude"],
        "longitude":        coords["longitude"],
        "current_weather":  True,          # gives us live data
    }
    
    response = requests.get(url, params=params)  # HTTP GET call
    
    if response.status_code == 200:              # 200 = success
        data = response.json()                   # convert JSON → dict
        weather = data["current_weather"]        # drill into the dict
        
        all_weather.append({
            "city":         city,
            "temperature":  weather["temperature"],   # in °C
            "windspeed":    weather["windspeed"],      # in km/h
            "weathercode":  weather["weathercode"],    # condition code
            "fetched_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        print(f"✅ Fetched: {city} → {weather['temperature']}°C")
    else:
        print(f"❌ Failed for {city}: {response.status_code}")

# ── 3. Save to CSV ─────────────────────────────────────────────
df = pd.DataFrame(all_weather)
df.to_csv("weather_data.csv", index=False)

print("\n📁 Saved to weather_data.csv")
print(df)