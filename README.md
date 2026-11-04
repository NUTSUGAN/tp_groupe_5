# Projet trafic aérien : exploration de la base

Analyse des vols au départ de New York (JFK, LGA, EWR) en 2021. Les données sont hébergées dans une base Postgres sur Supabase, et le script Python s'y connecte pour lancer des requêtes SQL.

## Installation

Prérequis : Python 3 installé.

1. Récupérer le projet :

```bash
git pull origin main
```

2. Créer l'environnement virtuel (une seule fois) :

```bash
python3 -m venv .venv
```

3. L'activer (à refaire à chaque nouveau terminal, sauf dans VS Code qui le fait seul) :

```bash
source .venv/bin/activate
```

Sous Windows : `.venv\Scripts\activate`

4. Installer les paquets :

```bash
pip install -r requirements.txt
```

## Connexion à la base

Le mot de passe n'est **jamais** dans le dépôt. Chacun crée son propre fichier `.env` à la racine du projet (il est ignoré par git) :

```
DATABASE_URL=postgresql://postgres.wvvbbaggdburoxpfymqz:MOT_DE_PASSE@aws-1-eu-central-1.pooler.supabase.com:5432/postgres?sslmode=require
```

- Remplace `MOT_DE_PASSE` par le mot de passe de la base, à demander à l'équipe en message privé.
- Pas de crochets, pas d'espaces, pas de guillemets.
- Si le mot de passe contient des caractères spéciaux (`@`, `#`, `/`…), il faut les encoder dans l'URL.

## Lancer le script

```bash
python main.py
```
