import copy
import numpy as np
import networkx as nx

from heuristique.heuristique_gloutonne import heuristique_gloutone
from heuristique.ordo_avec_liste import alloc_avec_liste
from objects.instance import Instance
from script.utils import vecteur_bier


def permutation_by_2_random(liste, nombre):
    tempo = copy.copy(liste)
    for i in range(nombre):
        index1, index2 = np.random.choice(liste, 2, replace=False)
        temp = tempo[index1]
        tempo[index1] = tempo[index2]
        tempo[index2] = temp
    return tempo


def permutation_by_2_all(liste):
    liste_permut = []
    for j in range(0, len(liste) - 1):
        for i in range(j, len(liste) - 1):
            tempo = copy.copy(liste)
            temp = tempo[j]
            tempo[j] = tempo[i + 1]
            tempo[i + 1] = temp
            liste_permut.append(tempo)
    return liste_permut


def decalage_all(liste):
    liste_decale = []
    for j in range(0, len(liste)):
        tempo = copy.copy(liste)
        liste_decale.append(np.roll(tempo, j))
    return liste_decale


def inversion_all(liste):
    liste_inverse = []
    for i in range(0, len(liste)):
        for j in range(len(liste), i + 1, -1):
            tempo = copy.copy(liste)
            tempo_head = tempo[:i]
            to_be_flipped = tempo[i:j]
            tempo_tail = tempo[j:]
            liste_inverse.append(np.concatenate((tempo_head,
                                                 np.flip(to_be_flipped),
                                                 tempo_tail)))
    return liste_inverse


def permutation_random(liste, nombre):
    liste_permut = []
    for i in range(nombre):
        liste_permut.append(np.random.permutation(liste))
    return liste_permut


def estimation_meilleur_voisin(instance, data, liste, graph=nx.MultiDiGraph()):
    optimum = instance.makeSpan
    if graph == "None":
        graph = nx.MultiDiGraph()
        graph.add_node('O', makespan=optimum)
    else:
        graph.add_node(optimum)

    change = "No"
    opti_liste = []
    methodes_voisinage = [inversion_all, decalage_all, permutation_by_2_all]
    # Calcul des voisins:
    for m in methodes_voisinage:
        voisins = m(liste)
        for v in voisins:
            instance = Instance(**data)
            alloc_avec_liste(instance, v)
            graph.add_node(instance.makeSpan)
            graph.add_edge(optimum, instance.makeSpan)

            # Si le voisin est meilleur que l'optimum
            if instance.makeSpan < optimum:
                opti_liste = v
                opti_inst = instance
                optimum = instance.makeSpan
                change = "Yes"

    if change == "Yes":
        return optimum, opti_liste, graph, opti_inst, change
    else:
        return optimum, liste, graph, instance, change


def estimation_n_meilleurs_voisins(instance, data, liste, root, graph="None", n=2):
    optimum = instance.makeSpan
    if graph == "None":
        graph = nx.MultiDiGraph()
        graph.add_node('O', makespan=optimum)
    else:
        graph.add_node(root, makespan=optimum)

    best_vois = []
    best_liste = {}
    methodes_voisinage = [inversion_all, decalage_all, permutation_by_2_all]

    # Calcul des voisins:
    for i, m in enumerate(methodes_voisinage):
        voisins = m(liste)
        for j, v in enumerate(voisins):
            instance = Instance(**data)
            alloc_avec_liste(instance, v)
            # Chaque voisinage est stocké dans le vecteur best_liste (nom de la méthode, numéro du voisin)
            best_liste[m.__name__[1] + ":" + str(j)] = [m, v, instance.makeSpan]

    # Trie selon le makespan et sélection des 3 premiers
    best_liste = sorted(best_liste.items(), key=lambda x: x[1][2])[:n]

    # Formatage des données
    for e in best_liste:
        best_vois.append((e[1][1], str(e[0]), root, e[1][2]))

    return best_vois


def exploration_voisinage(instance, data, depth=2, n=2, liste="None", verbose=1):
    graph = nx.MultiDiGraph()

    if liste == "None":
        if instance.state == "Not Solved":
            heuristique_gloutone(instance)
            liste = vecteur_bier(instance)
        else:
            liste = vecteur_bier(instance)

    optimum = instance.makeSpan
    root = str(liste)
    best_vois = estimation_n_meilleurs_voisins(instance, data, liste, str(liste), graph, n=2)
    for b in best_vois:
        v, dst, root, make = b

        graph.add_node(str(v), makespan=make)
        graph.add_edge(root, str(v), chemin=dst)
        explore_deeper(instance, data, v, dst, graph, n, 0, depth)




    return graph


def explore_deeper(instance, data, v, root, graph, n, i,depth):
    best_vois2 = estimation_n_meilleurs_voisins(instance, data, v, root, graph="None", n=2)

    for b2 in best_vois2:
        v2, dst2, root2, make2 = b2
        graph.add_node(str(v2), makespan=make2)
        graph.add_edge(str(v), str(v2), chemin=dst2)


        while i < depth:
           i  =i +1
           explore_deeper(instance, data, v2, root2, graph, n, i ,depth)
