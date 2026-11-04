"""Mission 1 : explorer les vols avec pandas. Lancer depuis le dossier du projet."""

import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    st.subheader("\n" + titre)
    st.dataframe(resultat, hide_index=True)


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
afficher("10 destinations les plus fréquentées", destinations.head(10))
afficher("10 destinations les moins fréquentées",
         destinations.sort_values("Vols").head(10))

vols_partis = vols[vols["dep_time"].notna()]
departs = vols_partis["tailnum"].value_counts().rename_axis("Avion").reset_index(name="Départs")
afficher("10 avions avec le plus de départs", departs.head(10))
afficher("10 avions avec le moins de départs", departs.sort_values("Départs").head(10))

# 3. Destinations desservies par compagnie
par_compagnie = vols.groupby("carrier")["dest"].nunique().reset_index(name="Destinations")
par_compagnie = par_compagnie.merge(compagnies, on="carrier", how="left")
afficher("Destinations par compagnie", par_compagnie.sort_values("Destinations", ascending=False))

par_origine = vols.groupby(["carrier", "origin"])["dest"].nunique().reset_index(name="Destinations")
par_origine = par_origine.merge(compagnies, on="carrier", how="left")
afficher("Destinations par compagnie et origine", par_origine)

# 4. Vols vers Houston et Seattle
houston = vols[vols["dest"].isin(["IAH", "HOU"])]
print("\nQuestion 4 — Nombre de vols vers Houston :", len(houston))
print("Aperçu des vols vers Houston :")
print(houston.head().to_string(index=False))

seattle = vols[(vols["dest"] == "SEA") & (vols["origin"].isin(["EWR", "JFK", "LGA"]))]
resume_seattle = pd.DataFrame({
    "Mesure": ["Vols", "Compagnies", "Avions uniques"],
    "Nombre": [len(seattle), seattle["carrier"].nunique(), seattle["tailnum"].nunique()]
})
afficher("Vols de New York vers Seattle", resume_seattle)

# 5. Nombre de vols par destination et tri alphabétique avec les noms
afficher("Nombre de vols par destination", destinations.sort_values("Vols", ascending=False))
vols_avec_noms = vols.merge(
    aeroports[["faa", "name"]].rename(columns={"faa": "dest", "name": "Destination"}),
    on="dest", how="left")
vols_avec_noms = vols_avec_noms.merge(
    aeroports[["faa", "name"]].rename(columns={"faa": "origin", "name": "Origine"}),
    on="origin", how="left")
vols_avec_noms = vols_avec_noms.merge(
    compagnies.rename(columns={"name": "Compagnie"}), on="carrier", how="left")
vols_tries = vols_avec_noms.sort_values(["Destination", "Origine", "Compagnie"])
print("\nVols triés par destination, origine et compagnie — aperçu :")
print(vols_tries.head().to_string(index=False))

# 6. Compagnies absentes d'une origine et compagnies couvrant toutes les destinations
origines_compagnie = vols.groupby("carrier")["origin"].nunique()
print("\nCompagnies qui n'opèrent pas depuis les trois aéroports :")
print(origines_compagnie[origines_compagnie < 3].to_string())

destinations_compagnie = vols.groupby("carrier")["dest"].nunique()
print("\nCompagnies qui desservent toutes les destinations :")
print(destinations_compagnie[destinations_compagnie == vols["dest"].nunique()].to_string())

liaisons = vols.groupby(["carrier", "origin", "dest"]).size().reset_index(name="Vols")
print("\nTableau des liaisons par compagnie, origine et destination — aperçu :")
print(liaisons.head().to_string(index=False))

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

# Afficher les graphiques à la fin, après les réponses dans le terminal.
par_compagnie.sort_values("Destinations").plot.barh(
    x="name", y="Destinations", legend=False, title="Destinations par compagnie")
plt.xlabel("Nombre de destinations")
plt.tight_layout()

par_origine.pivot(index="carrier", columns="origin", values="Destinations").plot.bar(
    title="Destinations par compagnie et aéroport de départ")
plt.ylabel("Nombre de destinations")
plt.tight_layout()
plt.show()
