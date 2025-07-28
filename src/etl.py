import requests
import sqlite3
import pandas as pd
from datetime import datetime
from src.config import API_KEY, CITY, URL, DB_PATH

def init_db():
    """
    Crée la table meteo dans la base SQLite si elle n'existe pas.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS meteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        temp REAL,
        humidity INTEGER,
        pressure INTEGER,
        wind_speed REAL,
        wind_deg INTEGER,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()

def fetch():
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(URL, params=params)
    response.raise_for_status()
    data = response.json()

    return {
        "city": CITY,
        "timestamp": datetime.utcfromtimestamp(data["dt"]),
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"].get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "wind_deg": data.get("wind", {}).get("deg"),
        "description": data["weather"][0]["description"] if data.get("weather") else None
    }

def transform(record):
    # Ici tu peux ajouter du nettoyage ou enrichissement si besoin
    return record

def load(record):
    conn = sqlite3.connect(DB_PATH)
    df = pd.DataFrame([record])
    df.to_sql("meteo", conn, if_exists="append", index=False)
    conn.close()

if __name__ == "__main__":
    init_db()
    record = fetch()
    clean = transform(record)
    load(clean)
    print("✔ Donnée insérée :", clean)
