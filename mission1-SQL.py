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


# Exemples de requête :
print(requete("select origin, count(*) as nb_vols from flights group by origin order by nb_vols desc"))

print(requete("""
    select d.name as destination, count(*) as nb_vols
    from flights f
    join airports d on d.faa = f.dest
    group by d.name
    order by nb_vols desc
    limit 10
"""))


# 1. Mission

# Question 1
print('Question 1 : ')

print(requete("""
    select
        (select count(*) from airports) as nb_aeroports,
        (select count(*) from flights) as nb_departs,
        (select count(distinct dest) from flights) as nb_destinations,
        (select count(*) from airports where dst = 'N') as nb_sans_heure_ete,
        (select count(distinct tzone) from airports) as nb_fuseaux,
        (select count(*) from airlines) as nb_compagnies,
        (select count(*) from planes) as nb_avions
"""))

# Question 2
print('Question 2 :')

print(requete("""
    select a.name as aeroport_plus_departs, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    group by a.name
    order by nb_vols desc
    limit 1
"""))

print(requete("""
    select a.name as destination, count(*) as nb_vols,
           round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
    from flights f
    join airports a on a.faa = f.dest
    group by a.name
    order by nb_vols desc
    limit 10
"""))

print(requete("""
    select a.name as destination, count(*) as nb_vols,
           round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
    from flights f
    join airports a on a.faa = f.dest
    group by a.name
    order by nb_vols asc
    limit 10
"""))

print(requete("""
    select f.tailnum, count(*) as nb_vols
    from flights f
    join planes p on p.tailnum = f.tailnum
    group by f.tailnum
    order by nb_vols desc
    limit 10
"""))

print(requete("""
    select p.model as avion, count(*) as nb_vols
    from flights f
    join planes p on p.tailnum = f.tailnum
    group by p.model
    order by nb_vols asc
    limit 10
"""))

# Question 4
print('Question 4 :')

print(requete("""
    select a.name as depart, f.dest as destination, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    where f.dest in ('IAH', 'HOU')
    group by a.name, f.dest
    order by nb_vols desc
"""))

print(requete("""
    select a.name as depart, f.dest as destination, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    where f.dest in ('IAH', 'HOU')
    group by a.name, f.dest
    order by nb_vols desc
"""))

print(requete("""
    select count(*) as nb_vols,
           count(distinct carrier) as nb_compagnies,
           count(distinct tailnum) as nb_avions
    from flights
    where origin in ('JFK', 'LGA', 'EWR') and dest = 'SEA'
"""))

# Question 5
print('Question 5 :')

print(requete("select dest, count(*) as nb_vols_vers from flights group by dest order by nb_vols_vers desc"))

print(requete("""
    select distinct d.name as destination, o.name as origine, al.name as compagnie
    from flights f
    join airports d on d.faa = f.dest
    join airports o on o.faa = f.origin
    join airlines al on al.carrier = f.carrier
    order by d.name, o.name, al.name
"""))


