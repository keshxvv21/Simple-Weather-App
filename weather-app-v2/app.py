"""
app.py — Flask Weather App
Uses OpenWeatherMap API for current weather + 5-day forecast.
"""

import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    res = requests.get(url, params=params, timeout=10)
    return res.json(), res.status_code


def get_forecast(city):
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "cnt": 40   # 5 days × 8 readings per day
    }
    res = requests.get(url, params=params, timeout=10)
    return res.json(), res.status_code


def parse_forecast(data):
    """Group forecast by day, pick midday reading for each day."""
    days = {}
    for item in data.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        day_key = dt.strftime("%Y-%m-%d")
        hour = dt.hour
        # Prefer reading closest to noon
        if day_key not in days or abs(hour - 12) < abs(days[day_key]["hour"] - 12):
            days[day_key] = {
                "hour": hour,
                "date": dt.strftime("%a, %d %b"),
                "temp_max": item["main"]["temp_max"],
                "temp_min": item["main"]["temp_min"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"],
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "pop": round(item.get("pop", 0) * 100),  # Probability of precipitation
            }
    # Return next 5 days (skip today)
    result = [v for v in days.values()]
    return result[:5]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please enter a city name."}), 400

    if not API_KEY or API_KEY == "your_api_key_here":
        return jsonify({"error": "API key not set. Please add your OpenWeatherMap API key to the .env file."}), 500

    # Current weather
    current_data, status = get_current_weather(city)
    if status != 200:
        msg = current_data.get("message", "City not found.").capitalize()
        return jsonify({"error": msg}), status

    # Forecast
    forecast_data, f_status = get_forecast(city)
    forecast = parse_forecast(forecast_data) if f_status == 200 else []

    # Build response
    result = {
        "city": current_data["name"],
        "country": current_data["sys"]["country"],
        "temp": round(current_data["main"]["temp"]),
        "feels_like": round(current_data["main"]["feels_like"]),
        "temp_min": round(current_data["main"]["temp_min"]),
        "temp_max": round(current_data["main"]["temp_max"]),
        "humidity": current_data["main"]["humidity"],
        "pressure": current_data["main"]["pressure"],
        "wind_speed": current_data["wind"]["speed"],
        "wind_deg": current_data["wind"].get("deg", 0),
        "visibility": round(current_data.get("visibility", 0) / 1000, 1),
        "description": current_data["weather"][0]["description"].title(),
        "icon": current_data["weather"][0]["icon"],
        "sunrise": datetime.fromtimestamp(current_data["sys"]["sunrise"]).strftime("%H:%M"),
        "sunset": datetime.fromtimestamp(current_data["sys"]["sunset"]).strftime("%H:%M"),
        "forecast": forecast,
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
