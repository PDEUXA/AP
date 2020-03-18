import argparse
import sys
import numpy as np
import os

from script.data import loader, separate
from docplex.cp.model import CpoModel
from config import setup


def main(argv):
    """
    :param argv: parser
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--instance",
        default="ft06",
        type=str,
        help="Nom de l'instance", )
    args = parser.parse_args()

    setup()
    recherche_exact(args.instance)


def recherche_exact(instance):
    '''
    :param instance: nom de l'instance str
    :return: None
    '''
    problem_data, optimum = loader(instance)
    nb_machine = problem_data["nb_machine"]
    nb_jobs = problem_data["nb_jobs"]
    problem = problem_data["problem"]

    machine, durations = separate(problem)

    model = CpoModel(name='Scheduling')

    # Variable
    job_operations = [[model.interval_var(size=durations[j][m],
                                          name="O{}-{}".format(j, m)) for m in range(nb_machine)] for j in
                      range(nb_jobs)]

    # chaque opération doit commencer aprés la fin de la précedente
    for j in range(nb_jobs):
        for s in range(1, nb_machine):
            model.add(model.end_before_start(job_operations[j][s - 1], job_operations[j][s]))

    # Pas d'overlap pour les operations executées sur une même machine
    machine_operations = [[] for m in range(nb_machine)]
    for j in range(nb_jobs):
        for s in range(0, nb_machine):
            machine_operations[machine[j][s]].append(job_operations[j][s])
    for lops in machine_operations:
        model.add(model.no_overlap(lops))

    # Minimiser la date de fin
    model.add(model.minimize(model.max([model.end_of(job_operations[i][nb_machine - 1]) for i in range(nb_jobs)])))

    # Solve model
    print("Solving model....")
    msol = model.solve(TimeLimit=10)


if __name__ == '__main__':
    main(sys.argv)
