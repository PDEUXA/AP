import numpy as np
from objects.instance import Instance
from objects.job import Job
from objects.task import Task


instance: Instance
j: Job
t: Task

def sort_task(instance, par="Start"):
    # Tries les taches selon la consigne (par date de début ou de fin)
    # Input: Objet de type Instance : instance
    # Output: Tableau (JobID, taskID, start, fin, prédécesseur) : task_list

    task_list = {}
    # Parcours des jobs de l'instance
    for j in instance.jobs_list:
        # Parcours de tâches du job j:
        for t in j.task_list:
            # Ajout de la tâche à la liste
            task_list[str(t.jobID)+ str(t.taskID)] = (t.jobID, t.taskID, t.startDate, t.finishDate)

    if par=='Start':
        task_list = sorted(task_list.items(), key=lambda x: x[1][2])
        return task_list
    elif par=="Finish":
        task_list = sorted(task_list.items(), key=lambda x: x[1][3])
        return task_list
    else:
        print("Critère de tri non valide")
        return None

def critical_path(instance):
    # Trouve le chemin critique
    # Input : Objet de type instance ou Tableau (JobID, taskID, start, fin, prédécesseur)
    # Output : Liste de tâche

    if type(instance) == Instance:
        task_list = sort_task(instance)
        task_list = np.array(task_list)
    if type(task_list) == list:
        task_list = np.array(task_list)

    # Rang des tâches et marges =
    rang = 0
    while rang != -1:
        break

