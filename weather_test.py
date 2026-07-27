import requests

# Coordinates for Toronto (you can change these for any city)
latitude = 43.65
longitude = -79.38

url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

response = requests.get(url)
data = response.json()

print("Full response:")
print(data)

current = data["current_weather"]
temperature = current["temperature"]
wind_speed = current["windspeed"]

print()
print(f"Current temperature: {temperature}°C")
print(f"Current wind speed: {wind_speed} km/h")