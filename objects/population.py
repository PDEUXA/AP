import hashlib
import operator
from objects.individus import Individu
from objects.instance import Instance
from script.data import loader

indv: Individu


class Population:
    def __init__(self, nom):
        self.data, self.optimum = loader(name=nom)
        self.nb_machine = self.data['nb_machine']
        self.nb_machine = self.data['nb_machine']
        self.nb_jobs = self.data['nb_jobs']
        self.problem = self.data['problem']
        self.instance = Instance(nom)
        self.nom = nom
        self.individu = []
        self.nombre = 0
        self.generation = 0
        self.elite = "N/A"
        self.opti = 100000
        self.change = False
        self.generationSsChgt = 0
        self.facteurMutation = (self.generationSsChgt) / 10

    def __str__(self):
        return self.nombre

    def add_Indv(self, individu):
        self.individu.append(individu)
        self._maj_Nombre()
        self.hash = self._hashed()

    def _maj_Nombre(self):
        self.nombre = len(self.individu)
        for indv in self.individu:
            if self.generation < indv.generation:
                self.generation = indv.generation
                self.change = False

    def MeanFit(self):
        temp = 0
        for i in self.individu:
            temp += i.fitness
        return temp / len(self.individu)

    def MaxFit(self):
        temp = []
        for i in self.individu:
            temp.append(i.fitness)
        return max(temp)

    def reset_Indv(self):
        for i in self.individu:
            del i
        self.individu = []

    def calc_Proba(self):
        temp_somme = 0
        for indv in self.individu:
            if self.opti > indv.cout:
                self.opti = indv.cout
                self.elite = indv
            temp_somme += indv.cout
        for indv in self.individu:
            indv.set_Proba((1 - indv.cout / temp_somme) / (self.nombre - 1))

    def calc_Proba_rg(self):
        self.individu = sorted(self.individu, key=operator.attrgetter('fitness'))
        for i, indv in enumerate(self.individu):
            if self.opti > indv.cout:
                self.opti = indv.cout
                self.elite = indv
                self.change = True
            indv.set_Proba((i + 1) / (self.nombre * (self.nombre + 1) / 2))

    def set_facteurMutation(self):
        if self.change:
            self.generationSsChgt = 0
        else:
            self.generationSsChgt += 1
            self.facteurMutation = 0.2 * (self.generationSsChgt + 1) * 10 / 4

    def _hashed(self):
        hash = hashlib.blake2s(str(self.individu).encode(),
                               key=b'AP', digest_size=4).hexdigest()
        return str(hash)
