# src/run_etl.py

import time
from src.etl import init_db, fetch, transform, load

def main():
    init_db()
    for _ in range(5):  # collecte 5 fois
        record = fetch()
        record = transform(record)
        load(record)
        print("✔ Donnée insérée :", record)
        time.sleep(60 * 10)  # pause 10 minutes

if __name__ == "__main__":
    main()
