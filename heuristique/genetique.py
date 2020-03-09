import random
import time

import numpy as np
from heuristique.heuristique_gloutonne import heuristique_gloutone
from heuristique.ordo_avec_liste import alloc_avec_liste
from objects.logger import Logger
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


def main_genetique(nom, selec=25, crois=100, gene=100):
    pop = Population(nom)
    genese(crois, pop)
    Fichier = Logger(pop.instance, "algo_génétique",
                     **{"nombre selection": selec, "nombre croisement": crois,
                        "nombre génération": gene, "Seed": pop.hash})

    temps1 = time.time()
    temps2, temps_opti = 0, 0
    alert = 0
    meanfit = []
    maxfit = []
    while pop.generation <= gene and temps2 < 900 and alert < int(gene * 0.3):
        print("Géneration: ", pop.generation, file=open(Fichier.location, 'a'))
        evaluation(pop)
        selection(pop, selec)
        meanfit.append(pop.MeanFit())
        maxfit.append(pop.MaxFit())
        croisement(pop, n=crois)
        evaluation(pop)

        if pop.change == True:
            alert = 0
            print("==========================Nouvel elite !==========================",
                  file=open(Fichier.location, 'a'))
            print(pop.elite, file=open(Fichier.location, 'a'))
            opti = pop.elite.cout
            opti_hash = pop.elite.hash
            temps_opti = time.time() - temps1
        else:
            alert += 1
    temps2 = time.time() - temps1

    Fichier.makespanFile(pop.elite.cout, pop.elite.sequence)
    Fichier.tpsFile(temps2)
    Fichier.tpsFile(temps_opti, "Optimum trouvé au bout de :")
    return meanfit, maxfit, temps_opti


def genese(n, population):
    # Génération de la population initiale
    # n , un entier, qui défini la taille de la population
    # population, un objet Population
    inst = Instance(population.nom)
    heuristique_gloutone(inst, verbose=0, prio="SPT", rnd=0)
    liste = vecteur_bier(inst)
    sequence = permutation_random(liste, n - 2)
    sequence.append(liste)
    heuristique_gloutone(inst, verbose=0, prio="LPT", rnd=0)
    liste = vecteur_bier(inst)
    sequence.append(liste)

    for i, seq in enumerate(sequence):
        indv = Individu(population, "Adam", "Eve", seq)
        population.add_Indv(indv)


def evaluation(population):
    # Evaluation d'une population (fitness et makeSpan), et mis à jour des probabilité de selection
    #   et du facteur de mutation
    # population, un objet Population

    for indv in population.individu:
        indv.set_Cout(alloc_avec_liste(Instance(population.nom), indv.sequence))
    population.calc_Proba_rg()
    population.set_facteurMutation()


def selection(population, n):
    # Sélection des meilleurs enfants, selection par roulette
    temp_proba = []
    for indv in population.individu:
        temp_proba.append(indv.proba)

    tirage = np.random.choice(population.individu, size=n, replace=False, p=temp_proba)
    # tirage = population.individu[-n:]
    population.reset_Indv()

    for indv in tirage:
        population.add_Indv(indv)
    # On ajoute 10% d'elite à la selection
    for i in range(int(n * 0.10)):
        indv = copy.copy(population.elite)
        indv.generation = population.generation
        population.add_Indv(indv)

    inst = Instance(population.nom)
    heuristique_gloutone(inst, verbose=0, prio="SPT", rnd=0)
    liste = vecteur_bier(inst)
    sequence = permutation_random(liste, int(n * 0.10))

    # On ajoute 10% d'aléatoire à la selection
    # for seq in sequence:
    #     indv = Individu(population, "Adam", "Eve", seq)
    #     indv.set_Cout(alloc_avec_liste(Instance(population.nom), indv.sequence))
    #     population.add_Indv(indv)

    population.calc_Proba_rg()


def croisement(population, alpha=0.85, n=1):
    # Cross over, choix du pere et de la mere par roulette
    temp_proba = []
    for indv in population.individu:
        temp_proba.append(indv.proba)

    enfant = []
    while len(enfant) <= n:
        rnd = random.random()
        if alpha > rnd:
            # Choix de l'opérateur de croissement
            rnd = random.randint(0, 2)
            pere, mere = np.random.choice(population.individu, size=2, replace=False, p=temp_proba)
            if rnd == 0:
                temp1, temp2 = croisement_1_point(pere, mere)
            elif rnd == 1:
                temp1, temp2 = croisement_2_points(pere, mere)
            elif rnd == 2:
                temp1, temp2 = croisement_jobs(pere, mere, population)

            enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp1)))
            mutation(enfant[-1], population)
            enfant[-1].croisement = True

            enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp2)))
            mutation(enfant[-1], population)
            enfant[-1].croisement = True

    for e in enfant:
        population.add_Indv(e)


def croisement_1_point(pere, mere):
    # Croisement en 1 point:
    temp1 = ['o'] * len(pere.sequence)
    temp2 = ['o'] * len(mere.sequence)
    pere_gene = decodage_gene(pere.sequence)
    mere_gene = decodage_gene(mere.sequence)
    point1 = np.random.randint(0, len(pere.sequence))
    for i, e1 in enumerate(pere_gene):
        if i < point1:
            if e1 not in temp1:
                temp1[i] = e1
    c = np.setdiff1d(mere_gene, temp1, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp1):
        if elem == 'o':
            temp1[j] = next(it)

    for i, e1 in enumerate(mere_gene):
        if i < point1:
            if e1 not in temp2:
                temp2[i] = e1
    c = np.setdiff1d(mere_gene, temp2, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp2):
        if elem == 'o':
            temp2[j] = next(it)

    return temp1, temp2


def croisement_2_points(pere, mere):
    # Croisement en 1 point:
    temp1 = ['o'] * len(pere.sequence)
    temp2 = ['o'] * len(mere.sequence)
    pere_gene = decodage_gene(pere.sequence)
    mere_gene = decodage_gene(mere.sequence)
    # Croisement en 2 points:
    points = np.random.choice(len(pere.sequence), size=2, replace=False)
    for i, e1 in enumerate(pere_gene):
        if i < min(points) or i > max(points):
            if e1 not in temp1:
                temp1[i] = e1
    c = np.setdiff1d(mere_gene, temp1, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp1):
        if elem == 'o':
            temp1[j] = next(it)

    for i, e1 in enumerate(mere_gene):
        if i < min(points) or i > max(points):
            if e1 not in temp2:
                temp2[i] = e1
    c = np.setdiff1d(mere_gene, temp2, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp2):
        if elem == 'o':
            temp2[j] = next(it)

    return temp1, temp2


def croisement_jobs(pere, mere, population):
    # Job Cross over :
    temp1 = ['o'] * len(pere.sequence)
    temp2 = ['o'] * len(mere.sequence)
    pere_gene = decodage_gene(pere.sequence)
    mere_gene = decodage_gene(mere.sequence)
    rnd = np.random.randint(0, 1 + 1, population.nb_jobs)
    for i, e1 in enumerate(pere_gene):
        if rnd[int(e1.split("-")[1])] == 1:
            if e1 not in temp1:
                temp1[i] = e1
    c = np.setdiff1d(mere_gene, temp1, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp1):
        if elem == 'o':
            temp1[j] = next(it)

    for i, e1 in enumerate(mere_gene):
        if rnd[int(e1.split("-")[1])] == 1:
            if e1 not in temp2:
                temp2[i] = e1
    c = np.setdiff1d(mere_gene, temp2, assume_unique=True)
    it = iter(c)
    for j, elem in enumerate(temp2):
        if elem == 'o':
            temp2[j] = next(it)

    return temp1, temp2


def mutation(enfant, population, beta=0.15):
    beta = beta * (1 + population.facteurMutation)
    # Mutation de l'enfant sur chaque gene, mutation aléatoire

    # mutation par inversion
    rnd = random.random()
    if rnd < beta:
        rnd1 = np.random.choice(range(len(enfant.sequence)), size=2, replace=False)

        tempo = copy.copy(enfant.sequence)
        tempo_head = tempo[:min(rnd1)]
        to_be_flipped = tempo[min(rnd1):max(rnd1)]
        tempo_tail = tempo[max(rnd1):]
        enfant.sequence = np.concatenate((tempo_head, np.flip(to_be_flipped), tempo_tail))

    # mutation par insertion
    rnd = random.random()
    if rnd < beta:
        rnd1 = np.random.choice(range(len(enfant.sequence)), size=2, replace=False)

        tempo = copy.copy(enfant.sequence)
        tempo = np.delete(tempo, max(rnd1))
        enfant.sequence = np.insert(tempo, min(rnd1), enfant.sequence[max(rnd1)])

    # mutation par permutation
    rnd = random.random()
    if rnd < beta:
        rnd1 = np.random.choice(range(len(enfant.sequence)), size=2, replace=False)
        temp = enfant.sequence[min(rnd1)]
        enfant.sequence[min(rnd1)] = enfant.sequence[max(rnd1)]
        enfant.sequence[max(rnd1)] = temp
        enfant.set_Mutation((min(rnd1), max(rnd1)))

    # mutation par décalage
    rnd = random.random()
    if rnd < beta:
        rnd1 = np.random.choice(range(len(enfant.sequence)), size=1, replace=False)
        tempo = copy.copy(enfant.sequence)
        tempo = np.roll(tempo, rnd1)
        enfant.sequence = tempo
        enfant.set_Mutation((min(rnd1), max(rnd1)))
