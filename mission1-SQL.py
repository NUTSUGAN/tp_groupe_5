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
# Nombre de vols par aéroport d'origine
print(requete("select origin, count(*) as nb_vols from flights group by origin order by nb_vols desc"))

# Les 10 destinations les plus desservies
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

# Nombre d'aéroports, de vols, de destinations, d'aéroports sans heure d'été, de fuseaux horaires, de compagnies et d'avions
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

# Aéroport de départ le plus emprunté
print(requete("""
    select a.name as aeroport_plus_departs, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    group by a.name
    order by nb_vols desc
    limit 1
"""))

# Les 10 destinations les plus prisées, avec le pourcentage
print(requete("""
    select a.name as destination, count(*) as nb_vols,
           round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
    from flights f
    join airports a on a.faa = f.dest
    group by a.name
    order by nb_vols desc
    limit 10
"""))

# Les 10 destinations les moins prisées, avec le pourcentage
print(requete("""
    select a.name as destination, count(*) as nb_vols,
           round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
    from flights f
    join airports a on a.faa = f.dest
    group by a.name
    order by nb_vols asc
    limit 10
"""))

# Les 10 avions qui ont le plus décollé
print(requete("""
    select f.tailnum, count(*) as nb_vols
    from flights f
    join planes p on p.tailnum = f.tailnum
    group by f.tailnum
    order by nb_vols desc
    limit 10
"""))

# Les 10 modèles d'avions qui ont le moins décollé
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

# Vols vers Houston (IAH ou HOU), par aéroport de départ
print(requete("""
    select a.name as depart, f.dest as destination, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    where f.dest in ('IAH', 'HOU')
    group by a.name, f.dest
    order by nb_vols desc
"""))

# Vols vers Houston (IAH ou HOU), par aéroport de départ (identique à la précédente)
print(requete("""
    select a.name as depart, f.dest as destination, count(*) as nb_vols
    from flights f
    join airports a on a.faa = f.origin
    where f.dest in ('IAH', 'HOU')
    group by a.name, f.dest
    order by nb_vols desc
"""))

# Vols de New York vers Seattle : nombre de vols, de compagnies et d'avions
print(requete("""
    select count(*) as nb_vols,
           count(distinct carrier) as nb_compagnies,
           count(distinct tailnum) as nb_avions
    from flights
    where origin in ('JFK', 'LGA', 'EWR') and dest = 'SEA'
"""))

# Question 5
print('Question 5 :')

# Nombre de vols par destination
print(requete("select dest, count(*) as nb_vols_vers from flights group by dest order by nb_vols_vers desc"))

# Vols triés par destination, aéroport d'origine et compagnie (ordre alphabétique)
print(requete("""
    select distinct d.name as destination, o.name as origine, al.name as compagnie
    from flights f
    join airports d on d.faa = f.dest
    join airports o on o.faa = f.origin
    join airlines al on al.carrier = f.carrier
    order by d.name, o.name, al.name
"""))

# Question 6
print('Question 6 :')

# Compagnies qui n'opèrent pas sur tous les aéroports d'origine
print(requete("""
    select al.name as compagnie,
           count(distinct f.origin) as nb_origines,
           string_agg(distinct f.origin, ', ' order by f.origin) as origines
    from airlines al
    left join flights f on f.carrier = al.carrier
    group by al.name
    having count(distinct f.origin) < (select count(distinct origin) from flights)
    order by nb_origines, compagnie
"""))

# Compagnies qui desservent l'ensemble des destinations
print(requete("""
    select al.name as compagnie, count(distinct f.dest) as nb_destinations
    from airlines al
    join flights f on f.carrier = al.carrier
    group by al.name
    having count(distinct f.dest) = (select count(distinct dest) from flights)
"""))

# Tableau des origines et des destinations pour l'ensemble des compagnies
print(requete("""
    select al.name as compagnie,
           string_agg(distinct f.origin, ', ' order by f.origin) as origines,
           count(distinct f.dest) as nb_destinations,
           string_agg(distinct f.dest, ', ' order by f.dest) as destinations
    from airlines al
    left join flights f on f.carrier = al.carrier
    group by al.name
    order by nb_destinations desc, compagnie
"""))

# Question 7
print('Question 7 :')

# Destinations desservies par une seule compagnie
print(requete("""
    select d.name as destination, max(al.name) as compagnie, count(*) as nb_vols
    from flights f
    join airports d on d.faa = f.dest
    join airlines al on al.carrier = f.carrier
    group by d.name
    having count(distinct f.carrier) = 1
    order by compagnie, destination
"""))

# Question 8
print('Question 8 :')

# Nombre de vols de United, American et Delta
print(requete("""
    select al.name as compagnie, count(*) as nb_vols
    from flights f
    join airlines al on al.carrier = f.carrier
    where f.carrier in ('UA', 'AA', 'DL')
    group by al.name
    order by nb_vols desc
"""))

# Les vols exploités par United, American ou Delta (20 premiers)
print(requete("""
    select al.name as compagnie, f.flight as num_vol, o.name as depart, d.name as arrivee,
           f.year, f.month, f.day
    from flights f
    join airlines al on al.carrier = f.carrier
    join airports o on o.faa = f.origin
    join airports d on d.faa = f.dest
    where f.carrier in ('UA', 'AA', 'DL')
    order by f.year, f.month, f.day, f.dep_time
    limit 20
"""))



