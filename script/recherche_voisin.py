import copy
import numpy as np


def permutation_by_2_random(liste, nombre):
    """
    Permutation de deux élements d'une liste
    :param liste: list
    :param nombre: int, nombre de permutation
    :return: list, liste permutée
    """
    tempo = copy.copy(liste)
    for i in range(nombre):
        index1, index2 = np.random.choice(liste, 2, replace=False)
        temp = tempo[index1]
        tempo[index1] = tempo[index2]
        tempo[index2] = temp
    return tempo


def permutation_by_2_all(liste):
    """
    liste de toutes les permutations
    :param liste: list
    :return: list, listes permutées
    """
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
    """
    liste de tout les décalages
    :param liste: list
    :return: listes décalée
    """
    liste_decale = []
    for j in range(0, len(liste)):
        tempo = copy.copy(liste)
        liste_decale.append(np.roll(tempo, j))
    return liste_decale


def inversion_all(liste):
    """
    liste de toutes les inversions
    :param liste: list
    :return: liste inversées
    """
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
    """
    permutation aléatoire d'une liste
    :param liste: list
    :param nombre: int, nombre de liste à générer
    :return: liste de liste
    """
    liste_permut = []
    for i in range(nombre):
        liste_permut.append(np.random.permutation(liste))
    return liste_permut

