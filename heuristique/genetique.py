import random
import time

import numpy as np
from heuristique.heuristique_gloutonne import heuristique_gloutone
from heuristique.ordo_avec_liste import alloc_avec_liste
from script.recherche_voisin import permutation_random
from script.utils import vecteur_bier, decodage_gene, codage_gene

from objects.individus import Individu
from objects.instance import Instance
from objects.population import Population
import copy
population: Population
indv: Individu
pere: Individu
mere: Individu
enfant: Individu

def main_genetique(pop, data, selec = 25, crois = 100, gene = 100):
    genese(crois, data, pop, data)
    temps1 = time.time()
    temps2 = 0
    while pop.generation <= gene and temps2 < 500:
        print("Géneration: ", pop.generation)
        evaluation(pop, data)
        selection(pop, selec)
        croisement(pop, n=crois)
        evaluation(pop, data)
        if pop.change == True:
            print("==========================Nouvel elite !==========================")
            print(pop.elite)
            print("Facteur demuta:", pop.facteurMutation)
    temps2 = time.time()-temps1
    print("Optimum :", pop.elite)
    print("Temps de recheche:", time.time()-temps1)

def genese(n, data, population):
    # Génération de la population initiale
    # n , un entier, qui défini la taille de la population
    inst = Instance(**data)
    heuristique_gloutone(inst, verbose=0, prio="SPT", rnd=0)
    liste = vecteur_bier(inst)
    sequence = permutation_random(liste, n)

    for i, seq in enumerate(sequence):
        indv = Individu(population, "Adam", "Eve", seq)
        population.add_Indv(indv)


def evaluation(population, data):
    for indv in population.individu:
        indv.set_Cout(alloc_avec_liste(Instance(**data), indv.sequence))
    population.calc_Proba_rg()
    population.has_Changed()


def selection(population, n):
    # Sélection des meilleurs enfants, selection par roulette
    temp_proba = []
    for indv in population.individu:
        temp_proba.append(indv.proba)
    # sorted_temp = sorted(temp.items(), key=lambda x: x[1][1])

    tirage = np.random.choice(population.individu, size=n, replace=False, p=temp_proba)
    population.reset_Indv()

    for indv in tirage:
        population.add_Indv(indv)
    # On ajoute 5 elite à la selction
    for i in range(int(n*0.1)):
        population.add_Indv(copy.copy(population.elite))

    population.calc_Proba_rg()


def croisement(population, alpha = 0.85, n = 1):
 #Cross over
    temp_proba = []
    for indv in population.individu:
        temp_proba.append(indv.proba)

    enfant = []
    while len(enfant) <= n:
        rnd = random.random()
        if alpha > rnd:
            pere, mere = np.random.choice(population.individu, size=2, replace=False, p=temp_proba)

            temp = ['o']*len(pere.sequence)
            pere_gene = decodage_gene(pere.sequence)
            mere_gene = decodage_gene(mere.sequence)

            rnd = np.random.randint(0, 1+1, population.nb_jobs)
            for i, e1 in enumerate(pere_gene):
                if rnd[int(e1[1])] == 1:
                    if e1 not in temp:
                        temp[i] = e1

            c = np.setdiff1d(mere_gene, temp, assume_unique = True)
            it = iter(c)
            for j, elem in enumerate(temp):
                if elem == 'o':
                    temp[j] = next(it)

            enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp)))
            mutation(enfant[-1],population)
            enfant[-1].croisement = True
    for e in enfant:
        population.add_Indv(e)


def mutation(enfant,population, beta=0.2):
    beta = beta / len(enfant.sequence) * (population.facteurMutation)
    # Mutation de l'enfant sur chaque gene, mutation aléatoire
    for i,gene in enumerate(enfant.sequence):
        rnd = random.random()
        if rnd < beta:
            rnd2 = random.randint(0, len(enfant.sequence)-1)
            copys = copy.copy(enfant.sequence)
            temp = enfant.sequence[i]
            enfant.sequence[i] = enfant.sequence[rnd2]
            enfant.sequence[rnd2] = temp
            enfant.set_Mutation((i, rnd2))
        else:
            pass



# def croisement(population, alpha = 0.8, operateur = 1):
#     # Croisement de deux individus, opérateur en 1 points (marche pas bien)
#     rnd = random.random()
#     temp_proba = []
#     for indv in population.individu:
#         temp_proba.append(indv.proba)
#
#     if operateur == 1:
#         if rnd < alpha:
#             pere, mere = np.random.choice(population.individu, size=2,  replace=False, p=temp_proba)
#
#             position_croisement = random.randint(0, len(pere.sequence))
#             seq1 = pere.sequence[:position_croisement]
#             seq2 = mere.sequence[position_croisement:]
#             enfant = Individu(population, pere, mere, sequence= np.concatenate([seq1,seq2]))
#             mutation(enfant)
#             enfant.croisement = True
#             population.add_Indv(enfant)
#
#     elif operateur == 2:
#         if rnd < alpha:
#             pere, mere = np.random.choice(population.individu, size=2, replace=False, p=temp_proba)
#
#             position_croisement = random.randint(0, len(pere.sequence))
#             position_croisement2 = random.randint(0, len(pere.sequence))
#             seq1 = pere.sequence[:position_croisement]
#             seq2 = mere.sequence[position_croisement:position_croisement2]
#             seq3 = pere.sequence[position_croisement2:]
#             enfant = Individu(population, pere, mere, sequence=np.concatenate([seq1, seq2, seq3]))
#             mutation(enfant)
#             enfant.croisement = True
#             population.add_Indv(enfant)
#
#
