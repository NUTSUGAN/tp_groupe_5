# Mission 1 — Exploration des données

## Question 1 — Combien y a-t-il d'aéroports, de compagnies, d'avions et de vols annulés ?

La table contient 1 458 aéroports. Les vols partent de trois aéroports de New York : EWR, JFK et LGA, et arrivent dans 103 destinations différentes. Parmi les aéroports de la table, 23 n'utilisent pas l'heure d'été. On trouve 10 fuseaux horaires et 16 compagnies aériennes.

Le registre contient 3 322 avions. Dans les vols, on trouve 3 982 numéros d'avion différents. Enfin, 6 481 vols n'ont pas d'heure réelle de départ. Je les considère comme annulés, car le fichier ne contient pas de colonne indiquant directement les annulations.

## Question 2 — Quels sont les aéroports, destinations et avions les plus ou les moins utilisés ?

L'aéroport de départ le plus fréquenté est EWR, avec 91 241 vols. JFK compte 83 119 départs et LGA en compte 78 344.

Les dix destinations les plus fréquentées sont Atlanta (ATL), avec 12 946 vols, Chicago O'Hare (ORD), avec 12 654 vols, Los Angeles (LAX), avec 11 895 vols, et Boston (BOS), avec 11 560 vols. Viennent ensuite Orlando (MCO), Charlotte (CLT), San Francisco (SFO), Fort Lauderdale (FLL), Miami (MIA) et Washington Reagan (DCA).

Atlanta représente environ 5,12 % des vols, Chicago O'Hare 5,01 %, Los Angeles 4,71 %, Boston 4,57 % et Orlando 4,21 %. Ces pourcentages sont calculés sur les 252 704 vols du fichier.

Les destinations les moins fréquentées sont Lexington (LEX), avec un seul vol, South Bend (SBN), avec quatre vols, puis Yampa Valley (HDN) et Montrose (MTJ), avec 15 vols chacune. Cherry Capital (TVC) compte 16 vols, Key West (EYW) 17, Palm Springs (PSP) 19, Gallatin Field (BZN) 20, Jackson Hole (JAC) 25 et Charlottesville (CHO) 31.

L'avion ayant effectué le plus de départs est N725MQ, avec 419 départs. Les suivants sont N723MQ (370), N713MQ (362), N711MQ (360) et N722MQ (358). Plusieurs avions sont à égalité avec un seul départ parmi les moins utilisés.

## Question 3 — Combien de destinations chaque compagnie dessert-elle ?

ExpressJet dessert 61 destinations différentes. Endeavor Air en dessert 47, United 45, JetBlue 42 et Delta 40. Envoy Air en dessert 20, American Airlines 19 et Southwest 11. Les autres compagnies desservent chacune cinq destinations ou moins.

Le nombre de destinations varie aussi selon l'aéroport de départ. Par exemple, Endeavor dessert 4 destinations depuis EWR, 34 depuis JFK et 36 depuis LGA. JetBlue en dessert respectivement 7, 42 et 6. Ces nombres comptent les destinations distinctes, pas le nombre de vols.

## Question 4 — Quels vols vont à Houston ? Combien vont à Seattle ?

Houston comprend les aéroports IAH et HOU. On compte 5 438 vols vers IAH et 1 520 vers HOU, soit 6 958 vols au total.

Depuis EWR, JFK et LGA, 2 736 vols vont à Seattle (SEA). Ils sont assurés par cinq compagnies et utilisent 856 avions différents dont le numéro est renseigné.

## Question 5 — Combien y a-t-il de vols par destination ? Comment les trier ?

Le fichier compte des vols vers 103 destinations. Les destinations ayant le plus de vols sont Atlanta (12 946), Chicago O'Hare (12 654), Los Angeles (11 895), Boston (11 560) et Orlando (10 637).

Pour présenter les vols dans l'ordre demandé, on associe à chaque code le nom de sa destination, de son aéroport de départ et de sa compagnie. On trie ensuite par nom de destination, puis par nom d'aéroport de départ, puis par nom de compagnie.

## Question 6 — Quelles compagnies n'opèrent pas depuis tous les aéroports ? Qui dessert toutes les destinations ?

Huit compagnies ne partent pas des trois aéroports de New York. Alaska, Frontier, AirTran, Hawaiian et Mesa n'apparaissent chacune que depuis un aéroport. SkyWest, Virgin America et Southwest apparaissent depuis deux aéroports.

Aucune compagnie ne dessert les 103 destinations présentes dans les données. Le tableau des liaisons permet de retrouver, pour chaque compagnie, ses aéroports de départ et ses destinations.

## Question 7 — Quelles destinations sont desservies par une seule compagnie ?

Certaines destinations ne sont desservies que par une compagnie dans ce fichier. Par exemple, Chicago Midway (MDW) est desservie par Southwest avec 3 096 vols. Piedmont Triad (GSO) est desservie par ExpressJet avec 1 199 vols, Akron Canton (CAK) par AirTran avec 622 vols, et John Wayne (SNA) par United avec 600 vols.

D'autres exemples sont Savannah (SAV) desservie par ExpressJet, Long Beach (LGB) par JetBlue, et Mercedita (PSE) par JetBlue. Ici, « exclusive » signifie qu'une seule compagnie apparaît pour la destination dans les données étudiées.

## Question 8 — Quels vols sont exploités par United, American ou Delta ?

United a effectué 44 165 vols, Delta 35 975 vols et American Airlines 24 602 vols.

## Remarque sur les données

Le fichier fourni contient 252 704 vols pour 2021, alors que l'énoncé parle de 326 776 vols. Les réponses ci-dessus sont calculées à partir des fichiers du projet. Les quatre destinations BQN, PSE, SJU et STT, absentes de la table des aéroports, sont nommées grâce aux informations données dans l'énoncé.
