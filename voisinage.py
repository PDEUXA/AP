import argparse
import sys
import time
import networkx as nx

from heuristique_gloutonne import heuristique_gloutonne
from objects.instance import Instance
from objects.logger import Logger
from objects.solution import Solution
from script.ordo_avec_liste import alloc_avec_liste
from script.utils import vecteur_bier


def main(argv):
    """
    :param argv: parser
    :return: None
    """
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--n",
        default=2,
        type=int,
        help="nombre de voisin", )
    parser.add_argument(
        "--max_depth",
        default=6,
        type=int,
        help="profondeur de l'exploration", )
    parser.add_argument(
        "--crit_stagnation",
        default=50,
        type=int,
        help="Nombre d'itération avant arrêt pour stagnation", )
    parser.add_argument(
        "--instance",
        default="ft06",
        type=str,
        help="nom de l'instance", )
    parser.add_argument(
        "--listonly",
        default=[],
        type=list,
        help="voisinage à partir d'une liste", )
    args = parser.parse_args()

    inst = Instance(args.instance)

    if not args.listonly:
        heuristique_gloutonne(inst, verbose=0, prio="SPT", rnd=0)
        liste_spt = vecteur_bier(inst)
        solution = Solution(inst, liste_spt)
    else:
        alloc_avec_liste(inst, args.listonly)

    exploration_voisinage(solution, args.n, args.max_depth, args.crit_stagnation)


def exploration_voisinage(solution, n=1, max_depth=6, crit_stagnation=50):
    """
    Explore le voisinage d'une solution
    :param solution: Solution
    :param n: int
    :param max_depth: int
    :param crit_stagnation: double
    :return: DiGraph
    """
    graph = nx.MultiDiGraph()
    temps1 = time.time()
    ecart = 10
    Fichier = Logger(solution.instance, "exploration_voisinage",
                     **{"n": n, "max_depth": max_depth, "crit_stagnation": crit_stagnation,
                        "Séquence de départ": solution.sequence})
    to_be_explored = []
    solution.voisinage()
    opti = solution.makeSpan

    to_be_explored.append(solution)
    graph.add_node(solution.nom, makespan=solution.makeSpan)
    depth, alert, compt = 0, 0, 0
    explored = []
    best = solution.sequence
    while to_be_explored:
        if depth < max_depth:
            if alert == crit_stagnation:
                Fichier.addLine("Stagnation du makespan")
                break
            else:
                depth = to_be_explored[0].depth
                to_be_explored, explored, make_min, seq = explore_deeper(depth, to_be_explored, explored, graph, n,
                                                                         Fichier)
            if make_min < opti:
                alert = 0
                opti = make_min
                best = seq
            else:
                alert += 1
            compt += 1
        else:
            Fichier.addLine("Profondeur atteinte")
            break

    temps = time.time() - temps1
    Fichier.makespanFile(opti, best)
    Fichier.itFile(compt)
    Fichier.tpsFile(temps)

    return graph


def explore_deeper(depth, to_be_explored, explored, graph, n, fichier):
    """
    :param depth: int
    :param to_be_explored: list
    :param explored: list
    :param graph: DiGraph
    :param n: int
    :param fichier: Fichier
    :return: list, list , int ,Solution
    """
    make = []
    origine = to_be_explored[0]
    origine.voisinage()
    best_vois = origine.best_vois(n)

    explored.append(origine.nom)
    to_be_explored.pop(0)
    for b in best_vois:
        if b.nom not in explored:
            to_be_explored.append(b)
            graph.add_node(b.nom, makespan=b.makeSpan)
            graph.add_edge(b.root.nom, b.nom, chemin=str(b.root.nom) + '/' + str(b.nom))
            ecart = round((origine.makeSpan - b.makeSpan) / origine.makeSpan, 3)
            make.append(b.makeSpan)
            print("Profondeur:", depth, ", Root: ", origine.nom, ", Voisinage: ",
                  b.nom, ", makeSpan: ", b.makeSpan, '/', origine.makeSpan,
                  ", écart: ", ecart, "%", file=open(fichier.location, 'a'))
        else:
            print("Deja exploré, Voisinage: ", b.nom, file=open(fichier.location, 'a'))
            ecart = 0
            make.append(b.makeSpan)

    return to_be_explored, explored, min(make), b


if __name__ == '__main__':
    main(sys.argv)
