import numpy as np

from heuristique.ordo_avec_liste import alloc_avec_liste
from objects.individus import Individu

indv: Individu

class Population:
    def __init__(self):
        self.individu = []
        self.nombre = 0

    def add_indv(self, individu):
        self.individu.append(individu)
        self.maj_nombre()

    def maj_nombre(self):
        self.nombre = len(self.individu)

    def reset_indv(self):
        self.individu = []