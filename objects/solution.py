import hashlib
import operator

from heuristique.ordo_avec_liste import alloc_avec_liste
from objects.instance import Instance
from script.recherche_voisin import inversion_all, decalage_all, permutation_by_2_all


class Solution:
    def __init__(self, data, sequence, root= "None"):
        self.root = root
        self.sequence = sequence
        self.nom = self._hashed()
        self.data = data
        self.voisin = []
        self.methodes_voisinage = [inversion_all, decalage_all, permutation_by_2_all]
        self.makeSpan = alloc_avec_liste(Instance(**self.data), self.sequence)
        if self.root == "None":
            self.depth = 0
        else:
            self.depth = self.root.depth + 1

    def __str__(self):
        return '{0},\n {1}'.format(self.sequence, self.makeSpan)

    def _hashed(self):
        hash = hashlib.blake2s(str(self.sequence).encode(), key=b'AP', digest_size=2).hexdigest()
        return str(hash)

    def voisinage(self):
        for i, m in enumerate(self.methodes_voisinage):
            voisins = m(self.sequence)
            for j, v in enumerate(voisins):
                voisin = Solution(self.data, v, self)
                self.voisin.append(voisin)

    def best_vois(self, n):
        if self.voisin:
            best = set(self.voisin)
            best = list(best)
            best = sorted(best, key=operator.attrgetter('makeSpan'))
            return best[:n]
        else:
            return None


