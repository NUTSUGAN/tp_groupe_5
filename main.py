import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env
load_dotenv()

# Récupère l'URL de connexion
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("DATABASE_URL manquante : ajoute-la dans le fichier .env")

# Connexion à la base
connection = psycopg2.connect(DATABASE_URL)


def requete(sql, params=None):
    """Exécute une requête SQL et renvoie le résultat dans un tableau pandas."""
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        colonnes = [c[0] for c in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=colonnes)


æ

