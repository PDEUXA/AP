from threading import Thread

from heuristique.genetique import croisement


class croiseur(Thread):

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
