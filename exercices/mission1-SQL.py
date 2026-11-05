"""Réponses SQL de la mission 1 sur la base PostgreSQL Supabase."""

import os
from contextlib import closing

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def ouvrir_base():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL manquante dans le fichier .env")
    return psycopg2.connect(url)


def executer(curseur, titre, requete):
    curseur.execute(requete)
    colonnes = [colonne.name for colonne in curseur.description]
    resultat = pd.DataFrame(curseur.fetchall(), columns=colonnes)
    print(f"\n{titre}")
    print(resultat.to_string(index=False))


def main():
    requetes = [
        (
            "Question 1 — Comptages",
            """
                select
                    (select count(*) from airports) as aeroports,
                    (select count(*) from flights) as vols,
                    (select count(distinct origin) from flights) as origines,
                    (select count(distinct dest) from flights) as destinations,
                    (select count(*) from airports where dst = 'N') as sans_heure_ete,
                    (select count(distinct tzone) from airports) as fuseaux,
                    (select count(*) from airlines) as compagnies,
                    (select count(*) from planes) as avions,
                    (select count(*) from flights where dep_time is null) as annulations
            """,
        ),
        (
            "Question 2 — Aéroports de départ",
            """
                select a.name as aeroport, count(*) as vols
                from flights f join airports a on a.faa = f.origin
                group by a.name order by vols desc
            """,
        ),
        (
            "Question 2 — Destinations les plus fréquentées",
            """
                select a.name as destination, count(*) as vols,
                       round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
                from flights f join airports a on a.faa = f.dest
                group by a.name order by vols desc limit 10
            """,
        ),
        (
            "Question 2 — Destinations les moins fréquentées",
            """
                select a.name as destination, count(*) as vols
                from flights f join airports a on a.faa = f.dest
                group by a.name order by vols limit 10
            """,
        ),
        (
            "Question 2 — Avions les plus utilisés",
            """
                select f.tailnum as avion, count(*) as vols
                from flights f join planes p on p.tailnum = f.tailnum
                where f.dep_time is not null
                group by f.tailnum order by vols desc limit 10
            """,
        ),
        (
            "Question 3 — Destinations par compagnie",
            """
                select al.name as compagnie, count(distinct f.dest) as destinations
                from flights f join airlines al on al.carrier = f.carrier
                group by al.name order by destinations desc
            """,
        ),
        (
            "Question 3 — Destinations par compagnie et origine",
            """
                select al.name as compagnie, f.origin,
                       count(distinct f.dest) as destinations
                from flights f join airlines al on al.carrier = f.carrier
                group by al.name, f.origin order by compagnie, f.origin
            """,
        ),
        (
            "Question 4 — Vols vers Houston",
            """
                select f.origin, f.dest, count(*) as vols
                from flights f where f.dest in ('IAH', 'HOU')
                group by f.origin, f.dest order by vols desc
            """,
        ),
        (
            "Question 4 — New York vers Seattle",
            """
                select count(*) as vols, count(distinct carrier) as compagnies,
                       count(distinct tailnum) as avions
                from flights
                where origin in ('EWR', 'JFK', 'LGA') and dest = 'SEA'
            """,
        ),
        (
            "Question 5 — Nombre de vols par destination",
            """
                select dest, count(*) as vols
                from flights group by dest order by vols desc
            """,
        ),
        (
            "Question 5 — Vols triés avec les libellés",
            """
                select distinct d.name as destination, o.name as origine,
                                al.name as compagnie
                from flights f
                join airports d on d.faa = f.dest
                join airports o on o.faa = f.origin
                join airlines al on al.carrier = f.carrier
                order by destination, origine, compagnie
            """,
        ),
        (
            "Question 6 — Compagnies absentes d'une origine",
            """
                select al.name as compagnie,
                       count(distinct f.origin) as origines,
                       string_agg(distinct f.origin, ', ' order by f.origin) as codes
                from airlines al left join flights f on f.carrier = al.carrier
                group by al.name
                having count(distinct f.origin) <
                       (select count(distinct origin) from flights)
                order by origines, compagnie
            """,
        ),
        (
            "Question 6 — Compagnies couvrant toutes les destinations",
            """
                select al.name as compagnie, count(distinct f.dest) as destinations
                from airlines al join flights f on f.carrier = al.carrier
                group by al.name
                having count(distinct f.dest) = (select count(distinct dest) from flights)
            """,
        ),
        (
            "Question 7 — Destinations à compagnie unique",
            """
                select d.name as destination, max(al.name) as compagnie, count(*) as vols
                from flights f
                join airports d on d.faa = f.dest
                join airlines al on al.carrier = f.carrier
                group by d.name
                having count(distinct f.carrier) = 1
                order by compagnie, destination
            """,
        ),
        (
            "Question 8 — United, American et Delta",
            """
                select al.name as compagnie, count(*) as vols
                from flights f join airlines al on al.carrier = f.carrier
                where f.carrier in ('UA', 'AA', 'DL')
                group by al.name order by vols desc
            """,
        ),
    ]

    with closing(ouvrir_base()) as connexion:
        with connexion.cursor() as curseur:
            for titre, requete in requetes:
                executer(curseur, titre, requete)


if __name__ == "__main__":
    main()
