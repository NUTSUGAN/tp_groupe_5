import os
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import psycopg2

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

tab1, tab2, tab3 = st.tabs(["Panda", "SQL", "Mission 3 — Tableau de bord"])

with tab1:
    # Charger les vols. Dans Excel, chaque ligne du CSV est rangée dans une seule cellule.
    colonne_vols = pd.read_excel("data/flights.xlsx", dtype=str).iloc[:, 0]
    texte_vols = "\n".join([colonne_vols.name] + colonne_vols.dropna().tolist())
    vols = pd.read_csv(io.StringIO(texte_vols), dtype=str)
    vols = vols.apply(lambda colonne: colonne.str.strip()).replace("", pd.NA)

    # Charger les informations de référence.
    aeroports = pd.read_excel("data/airports.xlsx").drop(columns="Unnamed: 0")
    compagnies = pd.read_json("data/airlines.json")
    avions = pd.read_html("data/planes.html")[0].drop(columns="Unnamed: 0")

    # Les heures vides sont utiles pour repérer les vols annulés.
    vols["dep_time"] = pd.to_numeric(vols["dep_time"], errors="coerce")

    # L'énoncé donne les noms de ces quatre aéroports absents du fichier airports.
    noms_manquants = pd.DataFrame({
        "faa": ["BQN", "PSE", "SJU", "STT"],
        "name": ["Rafael Hernandez Airport", "Mercedita Airport",
                 "San Juan Airport", "Cyril E. King Airport"]
    })
    aeroports = pd.concat([aeroports, noms_manquants], ignore_index=True)


    def afficher(titre, resultat):
        """Afficher un tableau dans Streamlit."""
        st.subheader(titre)
        st.dataframe(resultat, hide_index=True)


    st.header("Partie pandas")

    # 1. Comptages
    comptages = pd.DataFrame({
        "Mesure": ["Aéroports référencés", "Origines", "Destinations", "Sans heure d'été",
                   "Fuseaux horaires", "Compagnies", "Avions dans le registre", "Vols annulés"],
        "Nombre": [len(aeroports) - 4, vols["origin"].nunique(), vols["dest"].nunique(),
                   (aeroports["dst"] == "N").sum(), aeroports["tzone"].nunique(),
                   len(compagnies), len(avions), vols["dep_time"].isna().sum()]
    })
    afficher("Question 1 — Comptages", comptages)

    # 2. Origines, destinations et avions les plus et moins fréquents
    afficher("Question 2 — Vols par aéroport de départ",
             vols["origin"].value_counts().rename_axis("Aéroport").reset_index(name="Vols"))

    destinations = vols["dest"].value_counts().rename_axis("faa").reset_index(name="Vols")
    destinations = destinations.merge(aeroports[["faa", "name"]], on="faa", how="left")
    destinations["Pourcentage"] = (destinations["Vols"] / len(vols) * 100).round(2)
    destinations = destinations.rename(columns={"faa": "Code", "name": "Destination"})
    afficher("Question 2 — 10 destinations les plus fréquentées", destinations.head(10))
    afficher("Question 2 — 10 destinations les moins fréquentées",
             destinations.sort_values("Vols").head(10))

    vols_partis = vols[vols["dep_time"].notna()]
    departs = vols_partis["tailnum"].value_counts().rename_axis("Avion").reset_index(name="Départs")
    afficher("Question 2 — 10 avions avec le plus de départs", departs.head(10))
    afficher("Question 2 — 10 avions avec le moins de départs", departs.sort_values("Départs").head(10))

    # 3. Destinations desservies par compagnie
    par_compagnie = vols.groupby("carrier")["dest"].nunique().reset_index(name="Destinations")
    par_compagnie = par_compagnie.merge(compagnies, on="carrier", how="left")
    afficher("Question 3 — Destinations par compagnie", par_compagnie.sort_values("Destinations", ascending=False))

    par_origine = vols.groupby(["carrier", "origin"])["dest"].nunique().reset_index(name="Destinations")
    par_origine = par_origine.merge(compagnies, on="carrier", how="left")
    afficher("Question 3 — Destinations par compagnie et origine", par_origine)

    # Question 3 : graphiques
    st.subheader("Question 3 — Graphique : destinations par compagnie")
    ax = par_compagnie.sort_values("Destinations").plot.barh(
        x="name", y="Destinations", legend=False)
    ax.set_xlabel("Nombre de destinations")
    ax.figure.tight_layout()
    st.pyplot(ax.figure)

    st.subheader("Question 3 — Graphique : destinations par compagnie et origine")
    ax = par_origine.pivot(index="carrier", columns="origin", values="Destinations").plot.bar()
    ax.set_ylabel("Nombre de destinations")
    ax.figure.tight_layout()
    st.pyplot(ax.figure)

    # 4. Vols vers Houston et Seattle
    houston = vols[vols["dest"].isin(["IAH", "HOU"])]
    st.subheader("Question 4 — Vols vers Houston")
    st.write("Nombre de vols vers Houston :", len(houston))
    st.dataframe(houston.head(), hide_index=True)

    seattle = vols[(vols["dest"] == "SEA") & (vols["origin"].isin(["EWR", "JFK", "LGA"]))]
    resume_seattle = pd.DataFrame({
        "Mesure": ["Vols", "Compagnies", "Avions uniques"],
        "Nombre": [len(seattle), seattle["carrier"].nunique(), seattle["tailnum"].nunique()]
    })
    afficher("Question 4 — Vols de New York vers Seattle", resume_seattle)

    # 5. Nombre de vols par destination et tri alphabétique avec les noms
    afficher("Question 5 — Nombre de vols par destination", destinations.sort_values("Vols", ascending=False))
    vols_avec_noms = vols.merge(
        aeroports[["faa", "name"]].rename(columns={"faa": "dest", "name": "Destination"}),
        on="dest", how="left")
    vols_avec_noms = vols_avec_noms.merge(
        aeroports[["faa", "name"]].rename(columns={"faa": "origin", "name": "Origine"}),
        on="origin", how="left")
    vols_avec_noms = vols_avec_noms.merge(
        compagnies.rename(columns={"name": "Compagnie"}), on="carrier", how="left")
    vols_tries = vols_avec_noms.sort_values(["Destination", "Origine", "Compagnie"])
    afficher("Question 5 — Vols triés par destination, origine et compagnie (aperçu)", vols_tries.head())

    # 6. Compagnies absentes d'une origine et compagnies couvrant toutes les destinations
    origines_compagnie = vols.groupby("carrier")["origin"].nunique()
    afficher("Question 6 — Compagnies absentes d'une origine", origines_compagnie[origines_compagnie < 3].reset_index())

    destinations_compagnie = vols.groupby("carrier")["dest"].nunique()
    afficher("Question 6 — Compagnies desservant toutes les destinations",
             destinations_compagnie[destinations_compagnie == vols["dest"].nunique()].reset_index())

    liaisons = vols.groupby(["carrier", "origin", "dest"]).size().reset_index(name="Vols")
    afficher("Question 6 — Liaisons par compagnie, origine et destination (aperçu)", liaisons.head())

    # 7. Destinations desservies par une seule compagnie
    nb_compagnies = vols.groupby("dest")["carrier"].nunique()
    codes_exclusifs = nb_compagnies[nb_compagnies == 1].index
    exclusives = vols[vols["dest"].isin(codes_exclusifs)]
    exclusives = exclusives.groupby("dest").agg(
        Compagnie=("carrier", "first"), Vols=("dest", "size")).reset_index()
    exclusives = exclusives.merge(
        aeroports[["faa", "name"]].rename(columns={"faa": "dest", "name": "Destination"}),
        on="dest", how="left")
    afficher("Question 7 — Destinations exclusives", exclusives.sort_values("Vols", ascending=False))

    # 8. Vols opérés par United (UA), American (AA) ou Delta (DL)
    trois_compagnies = vols[vols["carrier"].isin(["UA", "AA", "DL"])]
    resume = trois_compagnies.groupby("carrier").size().reset_index(name="Vols")
    resume = resume.merge(compagnies, on="carrier", how="left")
    afficher("Question 8 — Vols de United, American et Delta", resume)

with tab2:
    # Partie SQL
    st.header("Partie SQL")

    afficher("Question 1 — Comptages généraux", requete("""
        select
            (select count(*) from airports) as nb_aeroports,
            (select count(*) from flights) as nb_departs,
            (select count(distinct dest) from flights) as nb_destinations,
            (select count(*) from airports where dst = 'N') as nb_sans_heure_ete,
            (select count(distinct tzone) from airports) as nb_fuseaux,
            (select count(*) from airlines) as nb_compagnies,
            (select count(*) from planes) as nb_avions
    """))

    afficher("Question 2 — Aéroport de départ le plus emprunté", requete("""
        select a.name as aeroport_plus_departs, count(*) as nb_vols
        from flights f
        join airports a on a.faa = f.origin
        group by a.name
        order by nb_vols desc
        limit 1
    """))

    afficher("Question 2 — 10 destinations les plus prisées", requete("""
        select a.name as destination, count(*) as nb_vols,
               round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
        from flights f
        join airports a on a.faa = f.dest
        group by a.name
        order by nb_vols desc
        limit 10
    """))

    afficher("Question 2 — 10 destinations les moins prisées", requete("""
        select a.name as destination, count(*) as nb_vols,
               round(100.0 * count(*) / sum(count(*)) over (), 2) as pourcentage
        from flights f
        join airports a on a.faa = f.dest
        group by a.name
        order by nb_vols asc
        limit 10
    """))

    afficher("Question 2 — 10 avions les plus actifs", requete("""
        select f.tailnum, count(*) as nb_vols
        from flights f
        join planes p on p.tailnum = f.tailnum
        group by f.tailnum
        order by nb_vols desc
        limit 10
    """))

    afficher("Question 2 — 10 modèles les moins actifs", requete("""
        select p.model as avion, count(*) as nb_vols
        from flights f
        join planes p on p.tailnum = f.tailnum
        group by p.model
        order by nb_vols asc
        limit 10
    """))


    afficher("Question 3 — Destinations par compagnie", requete("""
        select al.name as compagnie, count(distinct f.dest) as nb_destinations
        from airlines al
        join flights f on f.carrier = al.carrier
        group by al.name
        order by nb_destinations desc
    """))

    afficher("Question 3 — Destinations par compagnie et origine", requete("""
        select al.name as compagnie, f.origin, count(distinct f.dest) as nb_destinations
        from airlines al
        join flights f on f.carrier = al.carrier
        group by al.name, f.origin
        order by compagnie, f.origin
    """))

    afficher("Question 4 — Vols vers Houston", requete("""
        select a.name as depart, f.dest as destination, count(*) as nb_vols
        from flights f
        join airports a on a.faa = f.origin
        where f.dest in ('IAH', 'HOU')
        group by a.name, f.dest
        order by nb_vols desc
    """))

    afficher("Question 4 — Vols New York → Seattle", requete("""
        select count(*) as nb_vols,
               count(distinct carrier) as nb_compagnies,
               count(distinct tailnum) as nb_avions
        from flights
        where origin in ('JFK', 'LGA', 'EWR') and dest = 'SEA'
    """))

    afficher("Question 5 — Nombre de vols par destination", requete("select dest, count(*) as nb_vols_vers from flights group by dest order by nb_vols_vers desc"))


    afficher("Question 5 — Vols triés par destination", requete("""
        select distinct d.name as destination, o.name as origine, al.name as compagnie
        from flights f
        join airports d on d.faa = f.dest
        join airports o on o.faa = f.origin
        join airlines al on al.carrier = f.carrier
        order by d.name, o.name, al.name
    """))

    afficher("Question 6 — Compagnies absentes d'une origine", requete("""
        select al.name as compagnie,
               count(distinct f.origin) as nb_origines,
               string_agg(distinct f.origin, ', ' order by f.origin) as origines
        from airlines al
        left join flights f on f.carrier = al.carrier
        group by al.name
        having count(distinct f.origin) < (select count(distinct origin) from flights)
        order by nb_origines, compagnie
    """))

    afficher("Question 6 — Compagnies desservant toutes les destinations", requete("""
        select al.name as compagnie, count(distinct f.dest) as nb_destinations
        from airlines al
        join flights f on f.carrier = al.carrier
        group by al.name
        having count(distinct f.dest) = (select count(distinct dest) from flights)
    """))

    afficher("Question 6 — Origines et destinations par compagnie", requete("""
        select al.name as compagnie,
               string_agg(distinct f.origin, ', ' order by f.origin) as origines,
               count(distinct f.dest) as nb_destinations,
               string_agg(distinct f.dest, ', ' order by f.dest) as destinations
        from airlines al
        left join flights f on f.carrier = al.carrier
        group by al.name
        order by nb_destinations desc, compagnie
    """))

    afficher("Question 7 — Destinations à compagnie unique", requete("""
        select d.name as destination, max(al.name) as compagnie, count(*) as nb_vols
        from flights f
        join airports d on d.faa = f.dest
        join airlines al on al.carrier = f.carrier
        group by d.name
        having count(distinct f.carrier) = 1
        order by compagnie, destination
    """))


    afficher("Question 8 — Vols United, American et Delta", requete("""
        select al.name as compagnie, count(*) as nb_vols
        from flights f
        join airlines al on al.carrier = f.carrier
        where f.carrier in ('UA', 'AA', 'DL')
        group by al.name
        order by nb_vols desc
    """))

    afficher("Question 8 — 20 premiers vols United, American, Delta", requete("""
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



with tab3:

    st.header("Mission 3 — Tableau de bord pour aider à la décision")
    st.write("Les indicateurs ci-dessous résument les vols observés en 2021.")

    # Charger les informations utiles depuis la base déjà utilisée dans ce fichier.
    vols_web = requete("""
        select month, sched_dep_time, dep_time, arr_delay, origin, dest, carrier
        from flights
        where year = 2021
    """)

    # Créer une colonne pour l'heure et repérer les retards et les annulations.
    vols_web["heure"] = (vols_web["sched_dep_time"] // 100).fillna(0).clip(0, 23).astype(int)
    vols_web["annule"] = vols_web["dep_time"].isna()
    vols_web["retard"] = vols_web["arr_delay"] > 15

    # Filtrer les résultats par aéroport de départ.
    origines_web = ["Tous"] + sorted(vols_web["origin"].dropna().unique())
    origine_web = st.selectbox("Aéroport de départ — Mission 3", origines_web)
    destinations_web = ["Toutes"] + sorted(vols_web["dest"].dropna().unique())
    destination_web = st.selectbox("Destination — Mission 3", destinations_web)
    compagnies_web = ["Toutes"] + sorted(vols_web["carrier"].dropna().unique())
    compagnie_web = st.selectbox("Compagnie — Mission 3", compagnies_web)

    vols_filtres_web = vols_web
    if origine_web != "Tous":
        vols_filtres_web = vols_filtres_web[vols_filtres_web["origin"] == origine_web]
    if destination_web != "Toutes":
        vols_filtres_web = vols_filtres_web[vols_filtres_web["dest"] == destination_web]
    if compagnie_web != "Toutes":
        vols_filtres_web = vols_filtres_web[vols_filtres_web["carrier"] == compagnie_web]

    # Afficher les principaux indicateurs.
    vols_arrives_web = vols_filtres_web[
        ~vols_filtres_web["annule"] & vols_filtres_web["arr_delay"].notna()
    ]
    if len(vols_arrives_web) > 0:
        taux_retard_web = vols_arrives_web["retard"].mean() * 100
        retard_moyen_web = vols_arrives_web["arr_delay"].mean()
    else:
        taux_retard_web = 0
        retard_moyen_web = 0

    taux_annulation_web = vols_filtres_web["annule"].mean() * 100
    colonne1_web, colonne2_web, colonne3_web, colonne4_web = st.columns(4)
    colonne1_web.metric("Nombre de vols", len(vols_filtres_web))
    colonne2_web.metric("Vols avec plus de 15 minutes de retard", f"{taux_retard_web:.1f}%")
    colonne3_web.metric("Vols annulés", f"{taux_annulation_web:.1f}%")
    colonne4_web.metric("Retard moyen à l'arrivée", f"{retard_moyen_web:.1f} min")

    # Observer comment les retards changent selon le mois.
    st.subheader("Retards par mois")
    retards_par_mois_web = vols_filtres_web.groupby("month")["retard"].mean() * 100
    st.line_chart(retards_par_mois_web.rename("Vols en retard (%)"))
    st.subheader("Retards selon l'heure de départ")
    retards_par_heure_web = vols_arrives_web.groupby("heure")["retard"].mean() * 100
    st.bar_chart(retards_par_heure_web.rename("Vols en retard (%)"))

    # Comparer les destinations et les compagnies selon leur taux de retard.
    colonne_dest_web, colonne_compagnie_web = st.columns(2)
    colonne_dest_web.subheader("Destinations où les retards sont fréquents")
    retards_destinations_web = (
        vols_arrives_web.groupby("dest")["retard"].mean().sort_values(ascending=False).head(10) * 100
    )
    colonne_dest_web.bar_chart(retards_destinations_web.rename("Vols en retard (%)"))
    colonne_compagnie_web.subheader("Compagnies où les retards sont fréquents")
    retards_compagnies_web = (
        vols_arrives_web.groupby("carrier")["retard"].mean().sort_values(ascending=False).head(10) * 100
    )
    colonne_compagnie_web.bar_chart(retards_compagnies_web.rename("Vols en retard (%)"))
