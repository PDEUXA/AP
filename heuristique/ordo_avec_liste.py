import numpy as np

from objects.instance import Instance
from script.utils import decodage_bier

instance: Instance

def finish(instance):
    for job in instance.jobs_list:
        if job.state == "Not Done":
            return False
    instance.set_state()
    return True


def allocation_dispomachine_ASAP(instance, liste, verbose=1):
    time = 0
    while time < 10000:
        if finish(instance):
            break
        if verbose > 1:
            print("===============")
            print("TEMPS: ", time)
            print("===============")
        if len(liste) == 0:
            break
        change = 0
        index = np.array([])
        # 1 Liberations des ressource si tâches terminé
        for i, elem in enumerate(liste):
            if instance.jobs_list[elem].state != "Done":  # si le jobs n'est pas fini
                if instance.jobs_list[elem].current_task.finishDate <= time:
                    # DESALLOCATION DE LA TACHE EN COURS DU JOB A LA MACHINE ASSOCIE
                    if verbose > 1:
                        print("Desallocation de la tache #",
                              instance.jobs_list[elem].current_task.taskID,
                              " du job #",
                              elem,
                              " à la machine",
                              instance.jobs_list[elem].current_task.machine.name)
                    instance.jobs_list[elem].current_task.deallocate_to_ressource("Done")
                    change = 1
        # 2 parcours des taches et placement sur les machines libres
        for i, elem in enumerate(liste):
            if instance.jobs_list[elem].state != "Done":  # si le jobs n'est pas fini
                if instance.jobs_list[elem].current_task.machine.state == "Free":
                    # ALLOCATION DE LA TACHE EN COURS DU JOB A LA MACHINE ASSOCIE
                    currentID = instance.jobs_list[elem].current_task.taskID
                    instance.jobs_list[elem].update_current_task(currentID, time)
                    if verbose > 1:
                        print("Allocation de la tache #",
                              instance.jobs_list[elem].current_task.taskID,
                              " du job #",
                              elem,
                              " à la machine",
                              instance.jobs_list[elem].current_task.machine.name)
                    # On les enlèves de la liste
                    np.append(index, i)
                    change = 1
        liste = np.delete(liste, index)

        time += 1
        instance.calcMakeSpan()

        if change == 1 and verbose > 1:
            for j in instance.jobs_list:
                print(j)
    return instance.makeSpan


def alloc_avec_liste(instance, liste):
    tasks = decodage_bier(liste)
    dict_job = {}
    for i in range(len(instance.jobs_list)):
        dict_job[i] = 0
    for t, j in zip(tasks, liste):
        instance.jobs_list[j].update_current_task(t,
                                                  max(dict_job[j],
                                                      instance.jobs_list[j].task_list[t].machine.freeDate))
        dict_job[j] = instance.jobs_list[j].current_task.finishDate
        instance.jobs_list[j].current_task.deallocate_to_ressource("Done")
    return instance.makeSpan
