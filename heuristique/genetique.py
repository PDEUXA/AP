from heuristique.heuristique_gloutonne import heuristique_gloutone
from heuristique.ordo_avec_liste import alloc_avec_liste
from script.recherche_voisin import permutation_random
from script.utils import vecteur_bier

from objects.individus import Individu
from objects.instance import Instance
from objects.population import Population

population: Population
indv: Individu
def genese(n, data, population, methode):
    # Génération de la population initiale
    # n , un entier, qui défini la taille de la population
    # methode, la méthode de génération de la population
    inst = Instance(**data)
    heuristique_gloutone(inst, verbose=0, prio="SPT", rnd=0)
    liste = vecteur_bier(inst)
    sequence = permutation_random(liste, n)

    for i,seq in enumerate(sequence):
        indv = Individu(i,"Adam","Eve",seq)
        print(population.nombre)
        population.add_indv(indv)

def evaluation(population,data):
    for indv in population.individu:
        indv.set_cout(alloc_avec_liste(Instance(**data), indv.sequence))


def selection(population, n):
    temp = {}
    for indv in population.individu:
        temp[str(indv.ID)] = indv.cout

    sorted_temp = sorted(temp.items(), key=lambda x: x[1])[:n]

    population.reset_indv()
    for indv in sorted_temp:
        population.add_indv(indv)


    pass
    # Sélection des meilleurs enfants

def mutation():

    pass
    # Mutation de l'enfant

def croisement(pere, mere, seq, nombre):
    # Croisement de deux individus