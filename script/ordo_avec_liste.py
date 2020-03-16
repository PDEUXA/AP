from objects.instance import Instance
from script.utils import decodage_bier

instance: Instance


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


def alloc_avec_liste(instance, liste):
    """
    Résolution d'une instance à partir d'une liste
    :param instance: Instance
    :param liste: list
    :return: double, makespan
    """
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
