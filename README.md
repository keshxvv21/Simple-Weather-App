# Simple Weather app 🌤️

A weather app I built using Python and Flask. You type in a city, it shows you the current weather along with a 5-day forecast. Uses the OpenWeatherMap API for data.

---

## What it shows

- Current temperature (feels like, min/max)
- Humidity, wind speed & direction, visibility, pressure
- Sunrise & sunset times with total day length
- 5-day forecast with rain probability
- Live clock in the header

---

## Stack

- Python + Flask (backend)
- OpenWeatherMap API
- Plain HTML/CSS/JS (no frameworks)

---

## Running it locally

You'll need Python 3.8+ and a free API key from [openweathermap.org](https://openweathermap.org/api).

```bash
git clone https://github.com/yourusername/simple-weather-app.git
cd simple-weather-app

python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install flask requests python-dotenv
```

Create a `.env` file in the root:

```
OPENWEATHER_API_KEY=your_key_here
```

Then run:

```bash
python3 app.py
```
Note: I have installed the Version 3.10.3 which is the current latest as of March 2026, the version may vary according to your Time of initialization.

Open `http://127.0.0.1:5000` in your browser.

> Note: New API keys take about 10–30 minutes to activate after signup.

---

## Project structure

```
simple-weather-app/
├── app.py
├── requirements.txt
├── .env.example
└── templates/
    └── index.html
```

---

## License

MIT
