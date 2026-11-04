# Projet trafic aérien : exploration de la base

Application en ligne : [groupe-5.streamlit.app](https://groupe-5.streamlit.app/)

Analyse des vols au départ de New York (JFK, LGA, EWR) en 2021. Les données sont hébergées dans une base Postgres sur Supabase, le script SQL s'y connecte pour lancer des requêtes, et le script pandas lit les fichiers du dossier `data/`.

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

## Structure du projet

- `exercices/` : les scripts de la mission 1 (`mission1-SQL.py` et `mission1_pd.py`), exécutés dans le terminal.
- `app.py` : le front Streamlit qui affiche les résultats pandas et SQL dans deux onglets.
- `data/` : les fichiers sources lus par pandas.
- `reponses/` : les réponses rédigées.

## Lancer les exercices

Depuis la racine du projet (les chemins vers `data/` sont relatifs).

Requêtes SQL (nécessite le fichier `.env`) :

```bash
python exercices/mission1-SQL.py
```

Requêtes pandas :

```bash
python exercices/mission1_pd.py
```

## Lancer le front Streamlit

```bash
streamlit run app.py
```
