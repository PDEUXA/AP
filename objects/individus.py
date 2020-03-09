import hashlib


class Individu:
    def __init__(self, population, pere, mere, sequence):
        self.cout = "N/A"
        self.proba = 0
        self.population = population
        self.__croisement = False
        self.__mutation = False
        self.pere = pere
        self.mere = mere
        self.__mutationplace = []
        self.sequence = sequence
        self.hash = hashlib.blake2s(str(self.sequence).encode(), key=b'AP', digest_size=2).hexdigest()

        if type(self.pere) != str:
            self.generation = max(self.pere.generation, self.mere.generation) + 1
        else:
            self.generation = self.population.generation

        if type(self.pere) == str:
            self.ID = str(self.generation) + '-' + self.hash + '-A&E '
        else:
            self.ID = str(self.generation) + '-' + self.hash + '//' + self.pere.hash + '/' + self.mere.hash

    def __str__(self):
        if type(self.pere) == str:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}, Proba: {} %'.format(self.ID, "Adam", "Eve",
                                                                              self.cout,
                                                                              str(round(self.proba, 3) * 100))
        else:
            return 'ID: {}, Pere: {}, Mere: {}, Cout: {}, Proba: {} %'.format(self.ID, self.pere.ID, self.mere.ID,
                                                                              self.cout,
                                                                              str(round(self.proba, 3) * 100))

    def set_Cout(self, cout):
        self.cout = cout
        self.fitness = 1 / self.cout

    def set_Proba(self, proba):
        self.proba = proba

    def set_Mutation(self, i):
        if not self.__mutation:
            self.__mutation = True
            self.ID = self.ID + '(m)'
        else:
            self.__mutationplace.append(i)
