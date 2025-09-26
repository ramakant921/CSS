import requests

# Your API key from OpenWeatherMap (signup free at https://openweathermap.org/api)
API_KEY = "import requests"

# Your API key from OpenWeatherMap (signup free at https://openweathermap.org/api)
API_KEY = ""
city = "Delhi"

# API URL with city and key
url = f"http://api.openweathermap.org/data/2.5/weather?q=delhi&appid=485b945d1ecd6c977471d1292666e32e&units=metric"

# Send request
response = requests.get(url)
data = response.json()

# Check if request was successful
if data["cod"] == 200:
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    print(f"🌍 City: {city}")
    print(f"🌤️ Weather: {weather}")
    print(f"🌡️ Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Speed: {wind_speed} m/s")

else:
    print("❌ Error fetching weather data. Check your API key or city name.")

city = "Delhi"

# API URL with city and key
url = f"http://api.openweathermap.org/data/2.5/weather?q=delhi&appid=485b945d1ecd6c977471d1292666e32e&units=metric"

# Send request
response = requests.get(url)
data = response.json()

# Check if request was successful
if data["cod"] == 200:
    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    print(f"🌍 City: {city}")
    print(f"🌤️ Weather: {weather}")
    print(f"🌡️ Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Speed: {wind_speed} m/s")

else:
    print("❌ Error fetching weather data. Check your API key or city name.")
