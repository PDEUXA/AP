import copy
import numpy as np
import networkx as nx
import hashlib

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


def exploration_voisinage(solution, data, n=1, max_depth=6):
    graph = nx.MultiDiGraph()
    ecart = 10
    to_be_explored = []
    solution.voisinage()
    to_be_explored.append(solution)
    graph.add_node(solution.nom, makespan=solution.makeSpan)
    depth = 0
    alert = 0
    while to_be_explored and depth < max_depth:
        if ecart < 0:
            alert += 1
            if alert == 30 and to_be_explored:
                print("Stagnation du makespan")
                break
        else:
            alert = 0
            depth = to_be_explored[0].depth
            to_be_explored, ecart = explore_deeper(to_be_explored, graph, n)

    return graph


def explore_deeper(to_be_explored, graph, n):
    origine = to_be_explored[0]
    origine.voisinage()
    best_vois = origine.best_vois(n)
    to_be_explored.pop(0)
    for b in best_vois:
        to_be_explored.append(b)
        graph.add_node(b.nom, makespan=b.makeSpan)
        graph.add_edge(b.root.nom, b.nom, chemin=str(b.root.nom) + '/' + str(b.nom))
        ecart = (origine.makeSpan - b.makeSpan) / origine.makeSpan
        print("Root: ", origine.nom, "Voisinage: ", b.nom, " ,makeSpan: ", b.makeSpan, '/', origine.makeSpan,
              " ,écart: ", ecart)
        print(b.sequence)
    return to_be_explored, ecart
