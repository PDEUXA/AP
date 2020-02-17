import numpy as np
import pandas as pd
from objects.instance import Instance
from objects.job import Job
from objects.task import Task

instance: Instance
j: Job
t: Task

def decodage_bier(liste):
    # decodage vecteur de Bierwith
    vect_decode = []
    temp = []
    for i, elem in enumerate(liste):
        temp.append(elem)
        vect_decode.append(temp.count(elem)-1)
    return np.array(vect_decode)


def decodage_gene(sequence):
    temp = []
    for j,t in zip(sequence, decodage_bier(sequence)):
        temp.append('o'+str(j)+str(t))
    return temp


def codage_gene(sequence):
    temp = []
    for e in sequence:
        temp.append(int(e[1]))
    return np.array(temp)


def vecteur_bier(instance, par = "Start"):
    # Input :
    # --- Objet de type Instance

    data = sort_task(instance, par=par)
    liste = np.array([int(x[0].split(".")[0]) for x in np.array(data)])

    for i in range(instance.nb_jobs):
        if len(np.where(liste == i)[0]) != instance.nb_machine:
            print("Erreur sur le nombre de tâche/machine")
    return np.array(liste)


def sort_task(instance, par="Finish", dataframe=False):
    # Tries les taches selon la consigne (par date de début ou de fin)
    # Input: Objet de type Instance : instance
    # Output: Tableau (JobID, taskID, start, fin, prédécesseur) : task_list

    task_lists = {}
    # Parcours des jobs de l'instance
    for j in instance.jobs_list:
        # Parcours de tâches du job j:
        for t in j.task_list:
            # Ajout de la tâche à la liste
            task_lists[str(t.jobID) + '.' + str(t.taskID)] = [t.jobID, t.taskID, t.startDate, t.finishDate, t.totalFloat]
    if par == 'Start':
        task_lists = sorted(task_lists.items(), key=lambda x: x[1][2])
    elif par == "Finish":
        task_lists = sorted(task_lists.items(), key=lambda x: x[1][3])
    elif par == "Job":
        task_lists = sorted(task_lists.items(), key=lambda x: x[1][0])
    elif par == "Marge":
        task_lists = sorted(task_lists.items(), key=lambda x: x[1][1])
    else:
        print("Critère de tri non valide")
        return None

    if dataframe:
        task_lists = [task_lists[i][1] for i in range(len(task_lists))]
        task_lists = pd.DataFrame(task_lists, columns=["JobID", "TaskID", "Start", "Fin", "Marge Totale"])
    return task_lists




