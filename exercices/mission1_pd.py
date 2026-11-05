"""Réponses de la mission 1 avec pandas."""

import io
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"


def charger():
    cellule = pd.read_excel(DATA / "flights.xlsx", dtype=str).iloc[:, 0]
    csv = "\n".join([cellule.name, *cellule.dropna().tolist()])
    flights = pd.read_csv(io.StringIO(csv), dtype=str).replace(r"^\s*$", pd.NA, regex=True)
    flights = flights.apply(lambda colonne: colonne.str.strip())
    flights["dep_time"] = pd.to_numeric(flights["dep_time"], errors="coerce")

    airports = pd.read_excel(DATA / "airports.xlsx").drop(
        columns="Unnamed: 0", errors="ignore"
    )
    airlines = pd.read_json(DATA / "airlines.json")
    planes = pd.read_html(DATA / "planes.html")[0].drop(
        columns="Unnamed: 0", errors="ignore"
    )
    airports = pd.concat(
        [
            airports,
            pd.DataFrame(
                {
                    "faa": ["BQN", "PSE", "SJU", "STT"],
                    "name": [
                        "Rafael Hernandez Airport",
                        "Mercedita Airport",
                        "San Juan Airport",
                        "Cyril E. King Airport",
                    ],
                }
            ),
        ],
        ignore_index=True,
    )
    return flights, airports, airlines, planes


def afficher(question, resultat):
    print(f"\n{question}")
    print(resultat.to_string(index=False))


def main():
    flights, airports, airlines, planes = charger()

    afficher(
        "Question 1 — Comptages",
        pd.DataFrame(
            {
                "Mesure": [
                    "Aéroports",
                    "Origines",
                    "Destinations",
                    "Sans heure d'été",
                    "Fuseaux horaires",
                    "Compagnies",
                    "Avions",
                    "Vols annulés",
                ],
                "Nombre": [
                    len(airports) - 4,
                    flights["origin"].nunique(),
                    flights["dest"].nunique(),
                    (airports["dst"] == "N").sum(),
                    airports["tzone"].nunique(),
                    len(airlines),
                    len(planes),
                    flights["dep_time"].isna().sum(),
                ],
            }
        ),
    )

    afficher(
        "Question 2 — Origines",
        flights["origin"].value_counts().rename_axis("Origine").reset_index(name="Vols"),
    )
    destinations = (
        flights.groupby("dest")
        .size()
        .rename("Vols")
        .reset_index()
        .merge(airports[["faa", "name"]], left_on="dest", right_on="faa", how="left")
        .drop(columns="faa")
        .rename(columns={"dest": "Code", "name": "Destination"})
    )
    destinations["Pourcentage"] = (destinations["Vols"] / len(flights) * 100).round(2)
    afficher("Question 2 — 10 destinations les plus fréquentées", destinations.nlargest(10, "Vols"))
    afficher("Question 2 — 10 destinations les moins fréquentées", destinations.nsmallest(10, "Vols"))

    appareils = (
        flights[flights["dep_time"].notna()]["tailnum"]
        .value_counts()
        .rename_axis("Avion")
        .reset_index(name="Départs")
    )
    afficher("Question 2 — Avions avec le plus de départs", appareils.head(10))
    afficher("Question 2 — Avions avec le moins de départs", appareils.tail(10))

    compagnie_destinations = (
        flights.groupby("carrier")["dest"]
        .nunique()
        .rename("Destinations")
        .reset_index()
        .merge(airlines, on="carrier", how="left")
        .sort_values("Destinations", ascending=False)
    )
    afficher("Question 3 — Destinations par compagnie", compagnie_destinations)
    afficher(
        "Question 3 — Destinations par compagnie et origine",
        flights.groupby(["carrier", "origin"])["dest"]
        .nunique()
        .rename("Destinations")
        .reset_index(),
    )

    houston = flights[flights["dest"].isin(["IAH", "HOU"])]
    print(f"\nQuestion 4 — Vols vers Houston : {len(houston)}")
    print(houston.head().to_string(index=False))
    seattle = flights[
        flights["dest"].eq("SEA") & flights["origin"].isin(["EWR", "JFK", "LGA"])
    ]
    afficher(
        "Question 4 — New York vers Seattle",
        pd.DataFrame(
            {
                "Mesure": ["Vols", "Compagnies", "Avions uniques"],
                "Nombre": [
                    len(seattle),
                    seattle["carrier"].nunique(),
                    seattle["tailnum"].nunique(),
                ],
            }
        ),
    )

    afficher("Question 5 — Vols par destination", destinations.sort_values("Vols", ascending=False))
    avec_noms = flights.merge(
        airports[["faa", "name"]].rename(columns={"faa": "origin", "name": "Origine"}),
        on="origin",
        how="left",
    ).merge(
        airports[["faa", "name"]].rename(columns={"faa": "dest", "name": "Destination"}),
        on="dest",
        how="left",
    ).merge(airlines.rename(columns={"name": "Compagnie"}), on="carrier", how="left")
    afficher(
        "Question 5 — Vols triés par destination, origine et compagnie",
        avec_noms.sort_values(["Destination", "Origine", "Compagnie"]).head(20),
    )

    origines_par_compagnie = flights.groupby("carrier")["origin"].nunique()
    afficher(
        "Question 6 — Compagnies absentes d'une origine",
        origines_par_compagnie[origines_par_compagnie < 3]
        .rename("Nombre d'origines")
        .reset_index(),
    )
    couverture = flights.groupby("carrier")["dest"].nunique()
    afficher(
        "Question 6 — Compagnies couvrant toutes les destinations",
        couverture[couverture == flights["dest"].nunique()]
        .rename("Nombre de destinations")
        .reset_index(),
    )

    exclusifs = flights.groupby("dest")["carrier"].nunique()
    destinations_uniques = (
        flights[flights["dest"].isin(exclusifs[exclusifs == 1].index)]
        .groupby("dest")
        .agg(Compagnie=("carrier", "first"), Vols=("dest", "size"))
        .reset_index()
        .merge(airports[["faa", "name"]], left_on="dest", right_on="faa", how="left")
        .drop(columns="faa")
        .rename(columns={"name": "Destination"})
        .sort_values("Vols", ascending=False)
    )
    afficher("Question 7 — Destinations à compagnie unique", destinations_uniques)

    selection = flights[flights["carrier"].isin(["UA", "AA", "DL"])]
    afficher(
        "Question 8 — Vols United, American et Delta",
        selection.groupby("carrier")
        .size()
        .rename("Vols")
        .reset_index()
        .merge(airlines, on="carrier", how="left"),
    )


if __name__ == "__main__":
    main()
