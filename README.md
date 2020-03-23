# Utilisation 
## Methode exact:
CPLEX requis
````shell script
python methode_exacte.py --instance ft06

````

* "Nom de l'instance": instance



## Heuristique gloutonne
````shell script
python heuristique_gloutonne.py --instance ft06

````

* "Nom de l'instance": instance
* "SPT OU LPT" : prio
* "probabilité d'avoir un choix aléatoire dans l'heuristique": rnd


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

--> la sortie est un fichier texte dans Results/

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

--> la sortie est un fichier texte dans Results/