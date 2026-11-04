# Mission 1 — Exploration des données (réalisé en SQL par Gabriel)

## Question 1 — Combien y a-t-il d'aéroports, de compagnies, d'avions et de vols annulés ?

La table contient 1 462 aéroports : 1 458 viennent du fichier fourni et 4 ont été ajoutés (BQN, PSE, SJU et STT). Les vols partent de trois aéroports de New York : EWR, JFK et LGA, et arrivent dans 103 destinations différentes. Parmi les aéroports de la table, 23 n'utilisent pas l'heure d'été (`dst = 'N'`). On trouve 10 fuseaux horaires et 16 compagnies aériennes.

Le registre contient 4 038 avions : 3 322 viennent du fichier fourni et 716 ont été ajoutés avec leur seul numéro d'immatriculation (voir la remarque en fin de document). Dans les vols, on trouve 3 982 numéros d'avion différents. Enfin, 6 481 vols n'ont pas d'heure réelle de départ. Je les considère comme annulés, car la table ne contient pas de colonne indiquant directement les annulations.

## Question 2 — Quels sont les aéroports, destinations et avions les plus ou les moins utilisés ?

L'aéroport de départ le plus fréquenté est Newark Liberty (EWR), avec 91 241 vols. JFK compte 83 119 départs et LGA en compte 78 344.

Les dix destinations les plus fréquentées sont Atlanta (ATL), avec 12 946 vols, Chicago O'Hare (ORD), avec 12 654 vols, Los Angeles (LAX), avec 11 895 vols, et Boston (BOS), avec 11 560 vols. Viennent ensuite Orlando (MCO), Charlotte (CLT), San Francisco (SFO), Fort Lauderdale (FLL), Miami (MIA) et Washington Reagan (DCA).

Atlanta représente 5,12 % des vols, Chicago O'Hare 5,01 %, Los Angeles 4,71 %, Boston 4,57 % et Orlando 4,21 %. Ces pourcentages sont calculés sur les 252 704 vols de la table.

Les destinations les moins fréquentées sont Lexington (LEX), avec un seul vol, South Bend (SBN), avec quatre vols, puis Montrose (MTJ) et Yampa Valley (HDN), avec 15 vols chacune. Cherry Capital (TVC) compte 16 vols, Key West (EYW) 17, Palm Springs (PSP) 19, Gallatin Field (BZN) 20, Jackson Hole (JAC) 25 et Charlottesville (CHO) 31.

L'avion ayant effectué le plus de départs est N725MQ, avec 443 vols. Les suivants sont N723MQ (394), N713MQ (385), N722MQ (378) et N711MQ (376). Ces décomptes incluent les vols annulés. Plusieurs modèles d'avions n'ont qu'un ou deux vols, par exemple le Boeing 737-3A4, le 747-451, le 757-2B7 et l'Airbus A330-323, avec un seul vol chacun.

## Question 3 — Combien de destinations chaque compagnie dessert-elle ?

ExpressJet dessert 61 destinations différentes. Endeavor Air en dessert 47, United 45, JetBlue 42 et Delta 40. Envoy Air en dessert 20, American Airlines 19 et Southwest 11. Les autres compagnies desservent chacune cinq destinations ou moins.

Le nombre de destinations varie aussi selon l'aéroport de départ. Par exemple, Endeavor dessert 4 destinations depuis EWR, 34 depuis JFK et 36 depuis LGA. JetBlue en dessert respectivement 7, 42 et 6. Ces nombres comptent les destinations distinctes, pas le nombre de vols.

## Question 4 — Quels vols vont à Houston ? Combien vont à Seattle ?

Houston comprend les aéroports IAH et HOU. On compte 5 438 vols vers IAH et 1 520 vers HOU, soit 6 958 vols au total. Vers IAH, les vols partent d'EWR (3 024), de LGA (2 230) et de JFK (184). Vers HOU, ils partent d'EWR (739), de JFK (535) et de LGA (246).

Depuis EWR, JFK et LGA, 2 736 vols vont à Seattle (SEA). Ils sont assurés par cinq compagnies et utilisent 856 avions différents dont le numéro est renseigné.

## Question 5 — Combien y a-t-il de vols par destination ? Comment les trier ?

Les vols vont vers 103 destinations. Celles qui ont le plus de vols sont Atlanta (12 946), Chicago O'Hare (12 654), Los Angeles (11 895), Boston (11 560) et Orlando (10 637).

Pour présenter les vols dans l'ordre demandé, on joint la table des aéroports deux fois (une fois pour l'origine, une fois pour la destination) et la table des compagnies afin d'obtenir les noms complets. On trie ensuite par nom de destination, puis par nom d'aéroport de départ, puis par nom de compagnie. On obtient 431 combinaisons distinctes de destination, d'origine et de compagnie. La première est Akron Canton, depuis La Guardia, avec AirTran.

## Question 6 — Quelles compagnies n'opèrent pas depuis tous les aéroports ? Qui dessert toutes les destinations ?

Huit compagnies ne partent pas des trois aéroports de New York. AirTran, Frontier et Mesa n'apparaissent que depuis LGA, Alaska depuis EWR et Hawaiian depuis JFK. SkyWest et Southwest partent d'EWR et de LGA, et Virgin America d'EWR et de JFK.

Aucune compagnie ne dessert les 103 destinations présentes dans les données : la requête correspondante renvoie un tableau vide. La plus étendue, ExpressJet, en dessert 61. Le tableau des liaisons donne, pour chaque compagnie, ses aéroports de départ, le nombre de ses destinations et la liste de leurs codes.

## Question 7 — Quelles destinations sont desservies par une seule compagnie ?

29 destinations ne sont desservies que par une seule compagnie dans la table. Par exemple, Chicago Midway (MDW) est desservie par Southwest avec 3 096 vols. Piedmont Triad (GSO) est desservie par ExpressJet avec 1 199 vols, Savannah (SAV) par ExpressJet avec 598 vols, Akron Canton (CAK) par AirTran avec 622 vols, John Wayne (SNA) par United avec 600 vols, et Long Beach (LGB) par JetBlue avec 498 vols.

ExpressJet compte 11 de ces destinations et JetBlue 7. Mercedita (PSE) est exclusive à JetBlue avec 275 vols. Ici, « exclusive » signifie qu'une seule compagnie apparaît pour la destination dans les données étudiées.

## Question 8 — Quels vols sont exploités par United, American ou Delta ?

United a effectué 44 165 vols, Delta 35 975 vols et American Airlines 24 602 vols, soit 104 742 vols au total. On les retrouve en filtrant les vols sur les codes de compagnie UA, DL et AA.

## Remarque sur les données

La table contient 252 704 vols pour 2021, alors que l'énoncé parle de 326 776 vols. Les réponses ci-dessus sont calculées en SQL sur la base Supabase, qui contient les fichiers du projet.

Pour respecter les clés étrangères, 4 aéroports (BQN, PSE, SJU et STT), absents de la table des aéroports, ont été ajoutés avec le nom donné dans l'énoncé, et 716 avions présents dans les vols mais absents du registre ont été ajoutés avec leur seul numéro d'immatriculation. Leurs caractéristiques sont inconnues : cela concerne surtout les compagnies MQ (Envoy) et AA (American), dont les numéros ne figurent pas dans le registre FAA.
