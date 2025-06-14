# Multi-Agent AI System: SpaceX Launch Weather & News Analyzer

## 🌍 Project Overview

This project is a modular **Multi-Agent AI System** designed using the Google ADK pattern. It accepts a natural language goal and orchestrates a series of autonomous agents to:

1. **Identify** the next SpaceX launch.
2. **Fetch** weather data for the launch site.
3. **Enrich** the context with relevant news.
4. **Analyze** the likelihood of delay.
5. **Check** if the goal is satisfied.

## 🛠️ Architecture

```
User Goal
   ⬇
PlannerAgent
   ⬇
['SpaceXAgent', 'WeatherAgent', 'NewsAgent', 'AnalyzerAgent', 'GoalCheckerAgent']
   ⬇
Sequential execution of agents using shared state
```

## 🤖 Agents Description

### 📓 PlannerAgent

* Parses the goal string and returns an ordered execution plan.

### 🚀 SpaceXAgent

* Fetches the next SpaceX launch using the SpaceX API v3.
* Resolves launch site name to latitude and longitude using SpaceX API v4.

### ☀️ WeatherAgent

* Uses coordinates to fetch weather data via **OpenWeatherMap API**.

### 📰 NewsAgent

* Uses **NewsAPI** to fetch top headlines related to SpaceX and weather.

### 📊 AnalyzerAgent

* Analyzes the data to predict if the launch might be delayed.

### 🌿 GoalCheckerAgent

* Evaluates if the goal was fulfilled using analysis results.

## 🔧 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/yourname/multi-agent-spacex.git
cd multi-agent-spacex
```

### 2. Create `.env` File

```ini
OPENWEATHER_API_KEY=your_openweather_api_key
NEWSAPI_KEY=your_newsapi_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
python main.py
```

## 🌐 APIs Used

* [SpaceX API v3 & v4](https://github.com/r-spacex/SpaceX-API)
* [OpenWeatherMap API](https://openweathermap.org/api)
* [NewsAPI](https://newsapi.org/)

---

Made with ❤️ by Rishi Vejani
