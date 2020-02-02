import numpy as np
import pandas as pd
from objects.instance import Instance
from objects.job import Job
from objects.task import Task

instance: Instance
j: Job
t: Task


def sort_task(instance, par="Finish", dataframe=False):
    # Tries les taches selon la consigne (par date de début ou de fin)
    # Input: Objet de type Instance : instance
    # Output: Tableau (JobID, taskID, start, fin, prédécesseur) : task_list

    task_list = {}
    # Parcours des jobs de l'instance
    for j in instance.jobs_list:
        # Parcours de tâches du job j:
        for t in j.task_list:
            # Ajout de la tâche à la liste
            task_list[str(t.jobID) + str(t.taskID)] = [t.jobID, t.taskID, t.startDate, t.finishDate, t.totalFloat]

    if par == 'Start':
        task_list = sorted(task_list.items(), key=lambda x: x[1][2])
    elif par == "Finish":
        task_list = sorted(task_list.items(), key=lambda x: x[1][3])
    elif par == "Job":
        task_list = sorted(task_list.items(), key=lambda x: x[1][0])
    elif par == "Marge":
        task_list = sorted(task_list.items(), key=lambda x: x[1][1])
    else:
        print("Critère de tri non valide")
        return None

    if dataframe:
        task_list = [task_list[i][1] for i in range(len(task_list))]
        task_list = pd.DataFrame(task_list, columns=["JobID", "TaskID", "Start", "Fin", "Marge Totale"])
    return task_list




