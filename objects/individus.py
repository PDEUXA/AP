import hashlib
import random
import numpy as np


class Individu:
    def __init__(self, population, pere, mere, sequence):
        self.cout = "N/A"
        self.proba = 0
        self.population = population
        self.croisement = False
        self.mutation = False
        self.pere = pere
        self.mere = mere
        self.mutationplace= []
        if type(self.pere) != str:
            self.generation = max(self.pere.generation, self.mere.generation) + 1
        else:
            self.generation = self.population.generation

        self.sequence = sequence
        self.hash = hashlib.blake2s(str(self.sequence).encode(), key=b'AP', digest_size=2).hexdigest()

        if self.generation == 0:
            self.ID = str(self.generation) + '-' + self.hash + '-A&E '
        else:
            self.ID = str(self.generation) + '-' + self.hash + '//' + self.pere.hash + '/' + self.mere.hash

    def __str__(self):
        if type(self.pere) == str:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}, Proba: {} %'.format(self.ID, "Adam", "Eve",
                                                                            self.cout, round(self.proba,2) *100)
        else:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}, Proba: {}'.format(self.ID, self.pere.ID, self.mere.ID,
                                                                            self.cout, round(self.proba,2) *100)

    def __add__(self, other):
        self.population.generation += 1
        rnd = random.random()
        position_croisement = random.randint(0, len(self.sequence))
        if rnd > 0.5:
            seq1 = self.sequence[:position_croisement]
            seq2 = other.sequence[position_croisement:]
            return np.concatenate([seq1, seq2])
        else:
            return "Echec du croisement"

    def set_Cout(self, cout):
        self.cout = cout

    def set_Proba(self, proba):
        self.proba = proba

    def set_Mutation(self,i):
        if not self.mutation:
            self.mutation = True
            self.ID = self.ID + '(m)'
        else:
            self.mutationplace.append(i)

    def faisabilite(self):
        for i in range(self.population.nb_machine):
            if len(np.where(self.sequence == i)) != self.population.nb_machine:
                self.cout =  100000
                return False