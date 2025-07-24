import requests
import sqlite3
import pandas as pd
from datetime import datetime
from config import API_KEY, CITY, URL, DB_PATH
def init_db():
    """
    Crée la table meteo dans la base SQLite si elle n'existe pas.
    """
    # 1. Connexion (ouvre ou crée le fichier DB)
    conn = sqlite3.connect(DB_PATH)
    # 2. Exécution du DDL pour créer la table si besoin
    conn.execute("""
      CREATE TABLE IF NOT EXISTS meteo (
        timestamp DATETIME,
        temp REAL,
        humidity INTEGER
      )
    """)
    # 3. Enregistrement et fermeture
    conn.commit()
   
def fetch():
    params = {"q": CITY, "appid": API_KEY, "units": "metric"}
    response = requests.get(URL, params=params)
    response.raise_for_status()
    data = response.json()
    return {
        "timestamp": datetime.utcfromtimestamp(data["dt"]),
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"]
    }
    
