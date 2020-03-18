import argparse
import random
import sys

from objects.instance import Instance

inst: Instance


def main(argv):
    """
    :param argv: parser
    :return: None
    """
    parser = argparse.ArgumentParser()
    # Required arguments.
    parser.add_argument(
        "--prio",
        default="STP",
        type=str,
        help="SPT ou LPT", )
    parser.add_argument(
        "--instance",
        default="ft06",
        type=str,
        help="nom de l'instance", )
    parser.add_argument(
        "--rnd",
        default=0,
        type=float,
        help="tx de randomisation", )

    args = parser.parse_args()

    heuristique_gloutonne(Instance(args.instance), args.prio, args.rnd)


def recherche_tache(inst, t, prio="SPT", rnd=0):
    """
    Recherche la tâche prioritaire à un instant t, selon l'heuristique.
    :param inst: Instance
    :param t: int, temps
    :param prio: SPT ou LPT
    :param rnd: double 0<= : <= 1, % d'avoir une heuristique randomisé
    :return: None
    """

    tache_possible = []
    # Pour chaque jobs
    for j in inst.jobs_list:
        if j.state != "Done":
            # Si la machine de la tâche en cours du job et libre
            if j.current_task.machine.state == "Free":
                # On ajoute cette tache à la liste de tache possible
                tache_possible.append(j.current_task)
    if len(tache_possible) != 0:
        if random.random() < rnd:
            maxi_task = random.sample(tache_possible, 1)[0]
            mini_task = random.sample(tache_possible, 1)[0]
        # Recherche du max parmis les tâches possibles
        else:
            for k in range(len(tache_possible)):
                if prio == "LPT":
                    maxi = -1
                    for e in tache_possible:
                        if e.duration > maxi:
                            if e.machine.state == "Free":
                                maxi = e.duration
                                maxi_task = e
                elif prio == "SPT":
                    mini = 1000000
                    for e in tache_possible:
                        if e.duration < mini:
                            if e.machine.state == "Free":
                                mini = e.duration
                                mini_task = e
    try:
        if prio == "LPT":
            maxi_task.job.update_current_task(maxi_task.taskID, t)
            try:
                tache_possible.remove(maxi_task)
                return maxi_task
            except:
                pass
        elif prio == "SPT":
            mini_task.job.update_current_task(mini_task.taskID, t)
            try:
                tache_possible.remove(mini_task)
            except:
                pass
    except UnboundLocalError:
        pass


def finish(instance):
    """
    Vérifie si l'instance est résolue
    :param instance: Instance
    :return: Bool
    """
    for job in instance.jobs_list:
        if job.state == "Not Done":
            return False
    instance.set_state()
    return True


def heuristique_gloutonne(instance, prio="SPT", rnd=0, verbose=0):
    """
    Heuristique gloutonne
    :param instance: Instance
    :param prio: SPT OU LPT
    :param rnd: double, probabilité d'avoir un choix aléatoire dans l'heuristique
    :param verbose: int, niveau de verbose
    :return: None
    """
    time = 0
    while time < 10000:
        if finish(instance):
            break
        if verbose > 0:
            print("Temps", time)
        for res in instance.resource_list:
            if verbose > 0:
                print(res)
            if res.current_task == -1:
                recherche_tache(instance, time, prio, rnd)
            elif res.current_task.finishDate <= time:
                res.current_task.deallocate_to_ressource("Done")
                recherche_tache(instance, time, prio, rnd)
        time += 1
    instance.calcMakeSpan()
    return instance.makeSpan


if __name__ == '__main__':
    main(sys.argv)
