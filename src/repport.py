import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fonction 1 : Graphique des températures min, max, et moyennes par jour

def plot_weather_type_hist():
    conn = sqlite3.connect("data/meteo.db")
    df = pd.read_sql_query("SELECT weather_type FROM meteo", conn)
    conn.close()

    counts = df['weather_type'].value_counts()

    plt.figure(figsize=(8,5))
    counts.plot(kind='bar', color='skyblue')
    plt.title("Répartition des types de météo")
    plt.xlabel("Type de météo")
    plt.ylabel("Nombre d'enregistrements")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

# Fonction 3 : Graphique combiné température et humidité dans le temps (avec deux axes y)
def plot_temp_humidity():
    conn = sqlite3.connect("data/meteo.db")
    df = pd.read_sql_query("SELECT timestamp, temp, humidity FROM meteo", conn)
    conn.close()

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig, ax1 = plt.subplots(figsize=(10,6))

    ax1.plot(df['timestamp'], df['temp'], 'b-', label='Température (°C)')
    ax1.set_xlabel('Temps')
    ax1.set_ylabel('Température (°C)', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(df['timestamp'], df['humidity'], 'g-', label='Humidité (%)')
    ax2.set_ylabel('Humidité (%)', color='g')
    ax2.tick_params(axis='y', labelcolor='g')

    plt.title("Température et humidité dans le temps")
    fig.tight_layout()
    plt.show()

# Fonction 4 : Température moyenne par mois avec une ligne de tendance
def plot_monthly_avg_temp():
    conn = sqlite3.connect("data/meteo.db")
    df = pd.read_sql_query("SELECT date, temp FROM meteo", conn)
    conn.close()

    # Conversion de la colonne 'date' en datetime et extraction du mois et de l'année
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')

    # Calcul de la température moyenne par mois
    monthly_avg = df.groupby('month')['temp'].mean()

    # Vérification du nombre de mois différents
    print("Nombre de mois différents:", len(monthly_avg))

    if len(monthly_avg) > 1:
        # Régression linéaire si plus de 1 mois de données
        z = np.polyfit(range(len(monthly_avg)), monthly_avg, 1)
        p = np.poly1d(z)
        plt.plot(monthly_avg.index.astype(str), p(range(len(monthly_avg))), linestyle='--', label='Tendance')

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg.index.astype(str), monthly_avg, marker='o', label='Température Moyenne', color='coral')

    plt.title("Température Moyenne Mensuelle avec Tendance")
    plt.xlabel("Mois")
    plt.ylabel("Température Moyenne (°C)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Fonction 5 : Carte thermique des températures moyennes par mois et par année
def plot_heatmap_temp():
    conn = sqlite3.connect("data/meteo.db")
    df = pd.read_sql_query("SELECT date, temp FROM meteo", conn)
    conn.close()

    # Conversion de la colonne 'date' en datetime et extraction de l'année et du mois
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Pivot de la table pour créer une matrice avec les mois en colonnes et les années en lignes
    heatmap_data = df.pivot_table(index='year', columns='month', values='temp', aggfunc='mean')

    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, cmap='coolwarm', aspect='auto', interpolation='nearest')
    plt.colorbar(label="Température (°C)")
    plt.title("Carte Thermique des Températures Moyennes")
    plt.xlabel("Mois")
    plt.ylabel("Année")
    plt.xticks(ticks=np.arange(len(heatmap_data.columns)), labels=heatmap_data.columns)
    plt.yticks(ticks=np.arange(len(heatmap_data.index)), labels=heatmap_data.index)
    plt.tight_layout()
    plt.show()

# Fonction 6 : Graphique en secteur des proportions de types de météo
def plot_weather_type_pie():
    conn = sqlite3.connect("data/meteo.db")
    df = pd.read_sql_query("SELECT weather_type FROM meteo", conn)
    conn.close()

    counts = df['weather_type'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors[:len(counts)])
    plt.title("Répartition des Types de Météo")
    plt.axis('equal')  # Pour que le pie chart soit circulaire
    plt.tight_layout()
    plt.show()

# Lancer les fonctions
def generate_report():     # Graphique 1
    plot_weather_type_hist() # Graphique 2
    plot_temp_humidity()     # Graphique 3
    plot_monthly_avg_temp()  # Graphique 4
    plot_heatmap_temp()      # Graphique 5
    plot_weather_type_pie()  # Graphique 6

# Exécution du rapport
generate_report()
