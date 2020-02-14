from threading import Thread

from heuristique.genetique import croisement


class Croiseur(Thread):

    """Thread chargé simplement de croiser des individus"""

    def __init__(self,population,n):
        Thread.__init__(self)
        self.population = population
        self.n = n

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while self.population.nombre <= self.n:
            croisement(self.population)


class Voisineur(Thread):
    """Thread chargé simplement de croiser des individus"""

    def __init__(self,solution, methode):
        Thread.__init__(self)
        self.solution = solution
        self.methode = methode

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        temp = []
        voisins = self.methode(self.solution.sequence)
        for j, v in enumerate(voisins):
            voisin = Solution(self.data, v, self)
            temp.append(voisin)

        return temp

