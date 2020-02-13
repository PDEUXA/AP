import numpy as np

from heuristique.ordo_avec_liste import alloc_avec_liste
from objects.individus import Individu

indv: Individu

class Population:
    def __init__(self,**attributes):
        for attr_name, attr_value in attributes.items():
            setattr(self, attr_name, attr_value)
        self.individu = []
        self.nombre = 0
        self.generation = 0
        self.elite = "N/A"
        self.opti = 100000

    def __str__(self):
        return self.nombre

    def add_Indv(self, individu):
        self.individu.append(individu)
        self.maj_Nombre()

    def maj_Nombre(self):
        self.nombre = len(self.individu)
        for indv in self.individu:
            if self.generation < indv.generation:
                self.generation = indv.generation



    def reset_Indv(self):
        self.individu = []

    def calc_Proba(self):
        temp_somme = 0
        for indv in self.individu:
            if self.opti > indv.cout:
                self.opti = indv.cout
                self.elite = indv
            temp_somme += indv.cout
        for indv in self.individu:
            indv.set_Proba((1-indv.cout/temp_somme)/(self.nombre-1))