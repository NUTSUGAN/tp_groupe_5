import io
import pandas as pd
import matplotlib.pyplot as plt


# --- Lecture des fichiers ---
flights  = pd.read_excel("flights.xlsx")      
airports = pd.read_excel("airports.xlsx")     
airlines = pd.read_json("airlines.json")      
planes   = pd.read_html("planes.html")[0]     


# on recolle l'en-tête et toutes les lignes en un seul texte CSV
texte = "\n".join([flights.columns[0]] + flights.iloc[:, 0].astype(str).tolist())
# na_values=[" "] : dans ce fichier, une valeur manquante est un espace
flights = pd.read_csv(io.StringIO(texte), na_values=[" "])

# --- Q1 ---
# aéroports en tout (codes uniques dans la table airports)
print("Aéroports en tout   :", airports["faa"].nunique())
# aéroports de départ (valeurs uniques de origin)
print("Aéroports de départ :", flights["origin"].nunique())
# aéroports de destination (valeurs uniques de dest)
print("Destinations        :", flights["dest"].nunique())
# aéroports sans heure d'été (dst = "N")
print("Sans heure d'été (dst = N) :", (airports["dst"] == "N").sum())
# fuseaux horaires (le "\N" compte comme une valeur texte)
print("Fuseaux horaires           :", airports["tzone"].nunique())
# compagnies
print("Compagnies   :", flights["carrier"].nunique())
# avions différents (tailnum vides ignorés grâce à na_values)
print("Avions       :", flights["tailnum"].nunique())
# vols annulés = sans heure de départ
print("Vols annulés :", flights["dep_time"].isna().sum())


# --- Q2 ---
# aéroport de départ le plus emprunté
origines = flights["origin"].value_counts()
print("Aéroport de départ le plus emprunté :", origines.index[0], "avec", origines.iloc[0], "vols")

# nombre de vols par destination, avec le nom complet de l'aéroport
dest = flights.groupby("dest").size().rename("nb_vols").reset_index()
dest = dest.merge(airports[["faa", "name"]], left_on="dest", right_on="faa", how="left")
dest["name"] = dest["name"].fillna(dest["dest"])   # code gardé si le nom est absent
dest["pourcentage"] = (dest["nb_vols"] / dest["nb_vols"].sum() * 100).round(4)

# 10 destinations les plus prisées
print("\n10 destinations les plus prisées :")
print(dest.sort_values("nb_vols", ascending=False).head(10)[["dest", "name", "nb_vols", "pourcentage"]].to_string(index=False))

# 10 destinations les moins prisées
print("\n10 destinations les moins prisées :")
print(dest.sort_values("nb_vols").head(10)[["dest", "name", "nb_vols", "pourcentage"]].to_string(index=False))

# nombre de vols par avion
avions = flights["tailnum"].value_counts()

# 10 avions qui ont le plus décollé
print("\n10 avions qui ont le plus décollé :")
print(avions.head(10).to_string())

# 10 avions qui ont le moins décollé
print("\n10 avions qui ont le moins décollé :")
print(avions.sort_values().head(10).to_string())
print("Avions avec un seul vol :", (avions == 1).sum())


# --- Q3 ---
# nombre de destinations différentes desservies par chaque compagnie
dest_cie = flights.groupby("carrier")["dest"].nunique().rename("nb_destinations").reset_index()
# jointure avec airlines pour avoir le nom complet de la compagnie
dest_cie = dest_cie.merge(airlines, on="carrier").sort_values("nb_destinations", ascending=False)
print("Destinations desservies par compagnie :")
print(dest_cie[["carrier", "name", "nb_destinations"]].to_string(index=False))

# nombre de destinations par compagnie ET par aéroport d'origine
# unstack : les origines (EWR, JFK, LGA) deviennent des colonnes, 0 si la compagnie n'y opère pas
dest_cie_origine = flights.groupby(["carrier", "origin"])["dest"].nunique().unstack(fill_value=0)
print("\nDestinations desservies par compagnie et par aéroport d'origine :")
print(dest_cie_origine)

# Graphique 1 : destinations par compagnie (barres horizontales, de la plus grande à la plus petite)
plt.figure(figsize=(9, 6))
plt.barh(dest_cie["name"], dest_cie["nb_destinations"], color="#2a6f97")
plt.gca().invert_yaxis()                 # la plus grande en haut
plt.title("Nombre de destinations desservies par compagnie")
plt.xlabel("Nombre de destinations")
plt.tight_layout()
plt.savefig("graph_destinations_par_compagnie.png", dpi=150)

# Graphique 2 : destinations par compagnie et par aéroport d'origine (barres groupées)
dest_cie_origine = dest_cie_origine.loc[dest_cie["carrier"]]   # même ordre que le graphique 1
dest_cie_origine.plot(kind="bar", figsize=(11, 6), color=["#2a6f97", "#e9a03b", "#6a994e"])
plt.title("Destinations desservies par compagnie et par aéroport d'origine")
plt.xlabel("Compagnie")
plt.ylabel("Nombre de destinations")
plt.legend(title="Origine")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("graph_destinations_par_compagnie_origine.png", dpi=150)

plt.show()   # affiche les deux graphiques

# --- Q4 ---
# vols à destination de Houston (IAH ou HOU)
houston = flights[flights["dest"].isin(["IAH", "HOU"])]
print("Vols vers Houston (IAH ou HOU) :", len(houston))
print(houston["dest"].value_counts())

# parmi eux, ceux qui ont réellement atterri (heure d'arrivée renseignée)
atterris = houston[houston["arr_time"].notna()]
print("Vols ayant réellement atterri à Houston :", len(atterris))

# affichage des vols (colonnes principales)
print(atterris[["year", "month", "day", "carrier", "flight", "tailnum", "origin", "dest", "arr_time"]].head(10))

# vols des aéroports de New York (EWR, JFK, LGA) vers Seattle (SEA)
nyc_sea = flights[(flights["dest"] == "SEA") & (flights["origin"].isin(["EWR", "JFK", "LGA"]))]
print("\nVols NYC -> Seattle :", len(nyc_sea))
print(nyc_sea["origin"].value_counts())
# compagnies qui desservent Seattle
print("Compagnies vers Seattle :", nyc_sea["carrier"].nunique(), sorted(nyc_sea["carrier"].unique()))
# avions uniques (tailnum vides ignorés)
print("Avions uniques vers Seattle :", nyc_sea["tailnum"].nunique())


# --- Q5 ---
# nombre de vols par destination, avec le nom complet de l'aéroport
vols_dest = flights.groupby("dest").size().rename("nb_vols").reset_index()
vols_dest = vols_dest.merge(airports[["faa", "name"]], left_on="dest", right_on="faa", how="left")
vols_dest["name"] = vols_dest["name"].fillna(vols_dest["dest"])   # code gardé si le nom est absent
# tri alphabétique sur le nom de la destination (majuscules/minuscules ignorées)
vols_dest = vols_dest.sort_values("name", key=lambda s: s.str.lower())
print("Nombre de vols par destination (ordre alphabétique) :")
print(vols_dest[["dest", "name", "nb_vols"]].to_string(index=False))

# jointures pour obtenir les noms explicites : aéroport de destination, aéroport d'origine, compagnie
noms_dest = airports[["faa", "name"]].rename(columns={"faa": "dest", "name": "nom_destination"})
noms_orig = airports[["faa", "name"]].rename(columns={"faa": "origin", "name": "nom_origine"})
noms_cie  = airlines.rename(columns={"name": "nom_compagnie"})

vols = (flights
        .merge(noms_dest, on="dest", how="left")      # nom de la destination
        .merge(noms_orig, on="origin", how="left")    # nom de l'aéroport d'origine
        .merge(noms_cie, on="carrier", how="left"))   # nom de la compagnie
vols["nom_destination"] = vols["nom_destination"].fillna(vols["dest"])   # BQN, PSE, SJU, STT

# tri alphabétique croissant : destination, puis origine, puis compagnie (majuscules/minuscules ignorées)
vols = vols.sort_values(["nom_destination", "nom_origine", "nom_compagnie"],
                        key=lambda s: s.str.lower())

print("\nVols triés (destination, origine, compagnie) :")
print(vols[["nom_destination", "nom_origine", "nom_compagnie", "flight", "tailnum"]].head(20).to_string(index=False))

# export complet pour consulter les 252 704 lignes dans Excel
vols.to_csv("vols_tries.csv", index=False)

# --- Q6 ---
# nombre total d'origines et de destinations
nb_origines = flights["origin"].nunique()
nb_destinations = flights["dest"].nunique()

# tableau : pour chaque compagnie, l'ensemble de ses origines et de ses destinations
tableau = flights.groupby("carrier").agg(
    nb_origines=("origin", "nunique"),                                  # nombre d'origines
    nb_destinations=("dest", "nunique"),                                # nombre de destinations
    origines=("origin", lambda s: ", ".join(sorted(s.unique()))),       # liste des origines
    destinations=("dest", lambda s: ", ".join(sorted(s.unique()))),     # liste des destinations
).reset_index()
# nom complet de la compagnie
tableau = tableau.merge(airlines, on="carrier")

# compagnies qui n'opèrent pas sur tous les aéroports d'origine
print("Compagnies qui n'opèrent pas sur tous les aéroports d'origine :")
print(tableau[tableau["nb_origines"] < nb_origines][["carrier", "name", "origines"]].to_string(index=False))

# compagnies qui desservent l'ensemble des destinations
print("\nCompagnies qui desservent toutes les destinations :")
tout = tableau[tableau["nb_destinations"] == nb_destinations]
print(tout[["carrier", "name"]].to_string(index=False) if len(tout) else "Aucune")

# tableau complet origines / destinations pour chaque compagnie
print("\nTableau origines / destinations par compagnie :")
print(tableau[["carrier", "name", "nb_origines", "nb_destinations", "origines", "destinations"]].to_string(index=False))

# export pour consulter les listes complètes dans Excel
tableau.to_csv("compagnies_origines_destinations.csv", index=False)

# --- Q7 ---
# nombre de compagnies qui desservent chaque destination (et la compagnie, si une seule)
cie_par_dest = flights.groupby("dest")["carrier"].agg(nb_compagnies="nunique", carrier="first").reset_index()

# destinations desservies par une seule compagnie = exclusives
exclusives = cie_par_dest[cie_par_dest["nb_compagnies"] == 1]

# noms complets : aéroport de destination et compagnie
exclusives = exclusives.merge(airports[["faa", "name"]], left_on="dest", right_on="faa", how="left")
exclusives["name"] = exclusives["name"].fillna(exclusives["dest"])   # code gardé si le nom est absent
exclusives = exclusives.merge(airlines.rename(columns={"name": "compagnie"}), on="carrier")

# tri par compagnie puis par destination (majuscules/minuscules ignorées)
exclusives = exclusives.sort_values(["compagnie", "name"], key=lambda s: s.str.lower())

print("Nombre de destinations exclusives :", len(exclusives))
print(exclusives[["dest", "name", "compagnie"]].to_string(index=False))

# nombre de destinations exclusives par compagnie
print("\nDestinations exclusives par compagnie :")
print(exclusives.groupby("compagnie").size().sort_values(ascending=False))


# --- Q8 ---
# codes des 3 compagnies : UA = United, AA = American, DL = Delta
big3 = flights[flights["carrier"].isin(["UA", "AA", "DL"])]

# on ajoute le nom complet de la compagnie
big3 = big3.merge(airlines.rename(columns={"name": "compagnie"}), on="carrier", how="left")

print("Nombre de vols United, American ou Delta :", len(big3))
print("Part du total des vols :", round(len(big3) / len(flights) * 100, 2), "%")

# nombre de vols par compagnie
print("\nVols par compagnie :")
print(big3["compagnie"].value_counts())

# aperçu des vols filtrés
print("\nAperçu :")
print(big3[["year", "month", "day", "compagnie", "flight", "tailnum", "origin", "dest"]].head(10).to_string(index=False))

# export complet
big3.to_csv("vols_united_american_delta.csv", index=False)