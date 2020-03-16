# Utilisation 
## Recherche de voisinage:

````shell script
python voisinage.py --instance ft06

````

Les arguments:
* "Nom de l'instance": instance
* "Nombre de voisin": n, 
* "Profondeur d'exploration": max_depth, 
* "Nombre d'itération avant arrêt pour stagnation": crit_stagnation,
* "Séquence de départ": listonly

## Algorithme génétique:

````shell script
python genetique.py --ratiovoisin 0.2 --selec 100 --random False --crois 100 --gene 400 --beta 0.3 --multi 4

````

Les arguments:
* "Nom de l'instance": instance,
* "% de voisins de SPT et LPT": ratiovoisin,
* "Nombre selection": selec, 
* "Type de selection (random)": random, 
* "Nombre croisement": crois,
* "% de croisement": alpha, 
* "Type de croisement (duel)": duel,
* "Nombre génération": gene, 
* "Facteur de mutation": beta,
* "Affichage graphique": withgraph
* "Resolution de plusieurs instances": multi