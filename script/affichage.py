from itertools import count
import plotly.figure_factory as ff
import numpy as np
from objects.instance import Instance
from objects.job import Job
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib as mpl
from objects.resource import Resource

instance: Instance
j: Job
r: Resource


def plot_genetique_fitness(meanfit, maxfit, logger=None):
    """
    :param logger: Logger
    :param meanfit: list
    :param maxfit: list
    :return: None
    """
    title = ""
    if type(logger) == str:
        mpl.use('WebAgg')
        for i, (attr_name, attr_value) in enumerate(logger.attributes.items()):
            if (i + 1) % 3 == 0:
                title = title + str(attr_name) + ": " + str(attr_value) + "\n"
            else:
                title = title + str(attr_name) + ": " + str(attr_value) + ", "

    plt.plot(1 / np.array(meanfit), '-or', label="Makespan moyen")
    plt.plot(1 / np.array(maxfit), '-ob', label="Makespan mini")
    plt.legend()
    plt.xlabel('=======> Générations')
    plt.ylabel('=======> Makespan')
    plt.grid()
    title = logger

    plt.title(title)
    plt.show()
    plt.savefig(logger + ".png")


def plot_gantt(instance, by="JOB", grouping=True, color='Resource'):
    """
    Affiche le diagram de Gantt
    Input : Objet de type Instance
    # -- by : str, displaying by "JOB" or "MACHINE"
    # -- grouping = bool, grouping the display
    # -- colr = str, coloring by "Resource" or "Critical"
    :param instance: Instance
    :param by: "JOB" or "MACHINE"
    :param grouping: Bool
    :param color: "Resource"
    """

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
                               Critical=int(t.critical) * 100))

    elif by == "MACHINE":
        for r in instance.resource_list:
            for t in r.task_history:
                df.append(dict(Task="Machine  #" + str(t.machineID),
                               Start=datetime.fromordinal(t.startDate + 1),
                               Finish=datetime.fromordinal(t.finishDate + 1),
                               Resource="Job #" + str(t.jobID),
                               Critical=int(t.critical) * 100))

    fig = ff.create_gantt(df, index_col=color,
                          show_colorbar=True,
                          group_tasks=grouping,
                          show_hover_fill=True,
                          showgrid_x=True,
                          showgrid_y=True)
    fig.show()


def net_voisinage(graph):
    d_node = {}
    size = []
    for g in graph.nodes():
        d_node[g] = str(graph.nodes[g]['makespan']) + '-' + g
        size.append(graph.nodes[g]['makespan'])
    size = np.array(size) * 10 / size[0]
    groups = set(nx.get_node_attributes(graph, 'makespan').values())
    mapping = dict(zip(sorted(groups), count()))
    nodes = graph.nodes()

    colors = [mapping[graph.nodes[n]['makespan']] for n in nodes]
    plt.figure(figsize=(8, 8))
    pos = nx.planar_layout(graph)
    nx.draw(graph, pos, node_labels=d_node, node_color=colors,
            edge_color=range(graph.number_of_edges()), edge_cmap=plt.cm.jet,
            node_size=[i ** 3 for i in size], cmap=plt.cm.jet)
    nx.draw_networkx_labels(graph, pos, d_node)
    plt.show()
