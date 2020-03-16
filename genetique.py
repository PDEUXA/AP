import argparse
import operator
import random
import sys
import time
import multiprocess as mp
import numpy as np
from heuristique_gloutonne import heuristique_gloutonne
from script.ordo_avec_liste import alloc_avec_liste
from objects.logger import Logger
from script.affichage import plot_genetique_fitness
from script.recherche_voisin import permutation_random, permutation_by_2_random
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


def main(argv):
    """
    :param argv: parser
    :return: None
    """
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--instance",
        default="ft06",
        type=str,
        help="Nom de l'instance.", )
    parser.add_argument(
        "--ratiovoisin",
        default=0.5,
        type=float,
        help="% de voisins de SPT et LPT", )
    parser.add_argument(
        "--select",
        default=100,
        type=int,
        help="Nombre d'individu selectionné à chaque génération", )
    parser.add_argument(
        "--random",
        default=False,
        type=bool,
        help="Sélection aléatoire (True), élistique (False)", )
    parser.add_argument(
        "--crois",
        default=100,
        type=int,
        help="Nombre d'enfant à obtenir'", )
    parser.add_argument(
        "--alpha",
        default=0.85,
        type=float,
        help="Probabilité de croisement", )
    parser.add_argument(
        "--duel",
        default=True,
        help="Croisement par duel (True) ou par roulette (False)", )
    parser.add_argument(
        "--gene",
        default=100,
        type=int,
        help="Nombre de génération", )
    parser.add_argument(
        "--beta",
        default=0.15,
        type=float,
        help="Facteur de mutation", )
    parser.add_argument(
        "--withplot",
        default=False,
        type=bool,
        help="Affiche le graph de l\'évolution de la population", )
    parser.add_argument(
        "--multi",
        default=0,
        type=int,
        help="//isme", )
    args = parser.parse_args()

    if args.multi == 0:
        main_genetique(args.instance, args.ratiovoisin, args.select, args.random, args.crois, args.alpha, args.duel,
                       args.gene, args.beta, args.withplot)
    else:

        output = mp.Queue()

        for i in range(4):
            processes = [mp.Process(target=main_genetique, args=(args.instance, args.ratiovoisin,
                                                                 args.select, args.random, args.crois,
                                                                 args.alpha, args.duel,
                                                                 args.gene, args.beta, args.withplot)) for x in
                         range(args.multi)]
            for p in processes:
                p.start()
            for p in processes:
                p.join()


def main_genetique(nom, ratiovoisin=0.5, selec=100, random=False, crois=100,
                   alpha=0.85, duel=True, gene=100, beta=0.15, withplot=False):
    pop = Population(nom)
    temps1 = time.time()
    temps2, temps_opti = 0, 0
    alert = 0
    meanfit = []
    maxfit = []

    genese(crois, pop, ratio_voisin=ratiovoisin)
    fichier = Logger(pop.instance, "algo_génétique",
                     **{"% de voisins de SPT et LPT": ratiovoisin, "Nombre selection": selec,
                        "Type de selection (random)": random, "Nombre croisement": crois,
                        "% de croisement": alpha, "Type de croisement (duel)": duel,
                        "Nombre génération": gene, "Facteur de mutation": beta, "Seed": pop.hash})

    while pop.generation <= gene and temps2 < 900 and alert < int(gene * 0.3):
        print("Géneration: ", pop.generation, file=open(fichier.location, 'a'))

        evaluation(pop)
        selection(pop, selec, random=random)

        meanfit.append(pop.MeanFit())
        maxfit.append(pop.MaxFit())
        croisement(pop, alpha=alpha, beta=beta, duel=duel, n=crois)
        evaluation(pop)

        if pop.change:
            alert = 0
            print("==========================Nouvel elite !==========================",
                  file=open(fichier.location, 'a'))
            print(pop.elite, file=open(fichier.location, 'a'))
            temps_opti = time.time() - temps1
            pop.change = False
        else:
            alert += 1
    temps2 = time.time() - temps1

    fichier.makespanFile(pop.elite.cout, pop.elite.sequence)
    fichier.fitOverTIme(meanfit, maxfit)

    fichier.tpsFile(temps_opti, "Optimum trouvé au bout de: ")
    fichier.tpsFile(temps2, "Temps total: ")

    if withplot:
        plot_genetique_fitness(meanfit, maxfit, fichier)

    return meanfit, maxfit, temps_opti


def genese(n, population, ratio_voisin=0.5):
    """
    Génération de la population initiale
    n , un entier, qui défini la taille de la population
    population, un objet Population
    ratio voisin, le % d'individus voisins des heuristiques SPT et LPT
    :param n: Int
    :param ratio_voisin: Double 0<=:<=1
    :param population: Population
    """

    inst = Instance(population.nom)

    sequence = []
    # On ajoute le SPT et LPT à la population initiale et des permutations de SPT
    heuristique_gloutonne(inst, verbose=0, prio="SPT", rnd=0)
    liste_spt = vecteur_bier(inst)

    heuristique_gloutonne(inst, verbose=0, prio="LPT", rnd=0)
    liste_lpt = vecteur_bier(inst)

    for i in range(int(n * ratio_voisin)):
        rnd = random.randint(0, 2)
        if rnd > 1:
            sequence.append(permutation_by_2_random(liste_spt, 2))
        else:
            sequence.append(permutation_by_2_random(liste_lpt, 2))

    sequence.append(liste_lpt)
    sequence.append(liste_spt)

    sequence = sequence + permutation_random(liste_spt, (n - len(sequence)))

    # Instance des individus selon la séquence
    for seq in sequence:
        indv = Individu(population, "Adam", "Eve", seq)
        population.add_Indv(indv)


def evaluation(population):
    """
    Evaluation d'une population (fitness et makeSpan), et mis à jour des probabilité de selection
      et du facteur de mutation
    population, un objet Population
    :param population: Population
    """

    for indv in population.individu:
        indv.set_Cout(alloc_avec_liste(Instance(population.nom), indv.sequence))
    population.calc_Proba_rg()
    population.set_facteurMutation()


def selection(population, n, random=True):
    """
    Sélection des n individus dans la population,
    :type population: Population
    :param n: Int
    :param random: Bool
    """

    # Selection par roulette
    if random:
        temp_proba = []
        for indv in population.individu:
            temp_proba.append(indv.proba)

        tirage = np.random.choice(population.individu, size=n, replace=False, p=temp_proba)
        population.reset_Indv()

        # On ajoute 10% d'elite à la selection
        for i in range(int(n * 0.10)):
            indv = copy.copy(population.elite)
            indv.generation = population.generation
            population.add_Indv(indv)

    # Selection par élitisme
    else:
        population.individu = sorted(population.individu, key=operator.attrgetter('fitness'), reverse=True)
        tirage = population.individu[:n]
        population.reset_Indv()

    # Ajout des individus choisi
    for indv in tirage:
        population.add_Indv(indv)

    population.calc_Proba_rg()


def croisement(population, alpha=0.85, beta=0.15, duel=True, n=1):
    """
    Croisement d'une population jusqu'a obtenir n*alpha enfants, par duel (sans replacement) ou roulette (avec
    replacement)
    :param beta: Double 0<=:<=1, facteur de mutation
    :param n: Int
    :param duel: Bool
    :param alpha: Double 0<=:<=1, proba de croisement
    :type population: Population
    """
    enfant = []
    population.generation += 1

    # Croisement par roulette avec replacement
    if not duel:
        temp_proba = []
        for indv in population.individu:
            temp_proba.append(indv.proba)

        while len(enfant) <= n * alpha:
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
            mutation(enfant[-1], population, beta=beta)
            enfant[-1].croisement = True

            enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp2)))
            mutation(enfant[-1], population, beta=beta)
            enfant[-1].croisement = True


    # Croisement par duel sans replacement
    else:
        temp = copy.copy(population.individu)
        while len(enfant) <= n * alpha:
            if len(temp) > 1:
                rnd = random.randint(0, 2)
                # Duel du pere
                pere1, pere2 = np.random.choice(temp, size=2, replace=False)
                if pere1.cout >= pere2.cout:
                    pere = pere1
                    temp.remove(pere1)
                else:
                    pere = pere2
                    temp.remove(pere2)
                # Duel de la mere
                mere1, mere2 = np.random.choice(temp, size=2, replace=False)
                if mere1.cout >= pere2.cout:
                    mere = mere1
                    temp.remove(mere1)
                else:
                    mere = mere2
                    temp.remove(mere2)

                # Opérateur de croisement
                if rnd == 0:
                    temp1, temp2 = croisement_1_point(pere, mere)
                elif rnd == 1:
                    temp1, temp2 = croisement_2_points(pere, mere)
                elif rnd == 2:
                    temp1, temp2 = croisement_jobs(pere, mere, population)

                # Ajout des 2 enfants à la liste enfant
                enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp1)))
                mutation(enfant[-1], population)
                enfant[-1].croisement = True

                enfant.append(Individu(population, pere, mere, sequence=codage_gene(temp2)))
                mutation(enfant[-1], population)
                enfant[-1].croisement = True
            else:
                break
    # Ajout des enfants à la population
    for e in enfant:
        population.add_Indv(e)


def croisement_1_point(pere, mere):
    """
    Croisement en 1 point:
     :param pere: Individu
     :param mere: Individu
     """
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
    """
    Croisement en 1 point:
    :param pere: Individu
    :param mere: Individu
    """
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
    """
    Job Cross over :
    :param pere: Individu
    :param mere: Individu
    :param population:  Population
    """
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
    """
    Mutation de l'enfant
    :param beta: double 0=<:=<1
    :param population: Population
    :type enfant: Individu
    """
    beta = beta * (1 + population.facteurMutation)

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


if __name__ == '__main__':
    main(sys.argv)
