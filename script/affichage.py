import plotly.figure_factory as ff
import plotly.graph_objs as go
import numpy as np
from objects.instance import Instance
from objects.job import Job
from datetime import datetime
from script.utils import sort_task

from objects.resource import Resource

instance: Instance
j: Job
r: Resource


def plot_gantt(instance, by="JOB", grouping=True, color= 'Resource'):
    # Affiche le diagram de Gantt
    # Input : Objet de type Instance
    # -- by : str, displaying by "JOB" or "MACHINE"
    # -- grouping = bool, grouping the display
    # -- colr = str, coloring by "Resource" or "Critical"

    # df = [dict(Task="Job A", Start='2009-01-01', Finish='2009-02-01', Resource='Apple'),
    #      dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource='Grape'),
    #     dict(Task="Job C", Start='2009-04-20', Finish='2009-09-30', Resource='Banana')]

    # Création d'une liste de dictionnaire
    # Parcours les jobs de l'instance
    df = []
    if by == "JOB":
        for j in instance.jobs_list:
            # Parcours les tâches de jobs
            for t in j.task_list:
                # On associe chaque
                    df.append(dict(Task="Job  #" + str(t.jobID),
                                   Start=datetime.fromordinal(t.startDate + 1),
                                   Finish=datetime.fromordinal(t.finishDate + 1),
                                   Resource="Machine #" + str(t.machineID),
                                   Critical=int(t.critical)*100))

    elif by == "MACHINE":
        for r in instance.resource_list:
            for t in r.task_history:
                df.append(dict(Task="Machine  #" + str(t.machineID),
                               Start=datetime.fromordinal(t.startDate + 1),
                               Finish=datetime.fromordinal(t.finishDate + 1),
                               Resource="Job #" + str(t.jobID),
                               Critical=int(t.critical)*100))

    fig = ff.create_gantt(df, index_col=color,
                          show_colorbar=True,
                          group_tasks=grouping,
                          show_hover_fill=True,
                          showgrid_x=True,
                          showgrid_y=True)
    #fig.layout.xaxis.tickformat = '%'
    #go.FigureWidget(fig)
    fig.show()


def affichage_repetition(instance):
    # Input :
    # --- Objet de type Instance

    data = sort_task(instance)
    nb_machine = instance.nb_machine
    liste = [int(x[0][0]) for x in np.array(data)]
    for i in range(nb_machine):
        if liste.count(i) != nb_machine:
            print("Erreur sur le nombre de tâche/machine")

    return np.array(liste)





