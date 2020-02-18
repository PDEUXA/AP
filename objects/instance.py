from objects.job import Job
from objects.resource import Resource
from script.data import loader


class Instance:
    def __init__(self, nom):
        self.data, self.optimum = loader(name=nom)
        self.nb_machine = self.data['nb_machine']
        self.nb_jobs = self.data['nb_jobs']
        self.problem = self.data['problem']
        self.nom = nom
        self.resource_list = []
        self.jobs_list = []
        self.makeSpan = -1
        self.criticalPath = []
        self.state = "Not Solved"
        # Create Resources
        for i in range(self.nb_machine):
            self.resource_list.append(Resource(i))
        # Create jobs
        for i in range(self.nb_jobs):
            self.jobs_list.append(Job(i, self.problem[i], self.resource_list, self))

    def __str__(self):
        return '{}'.format(self.makeSpan)

    def set_state(self):
        self.state = "Solved"

    def calcMakeSpan(self):
        maxi = -1
        for j in self.jobs_list:
            for t in j.task_list:
                if type(t.finishDate) == str:
                    pass
                else:
                    if t.finishDate > maxi:
                        maxi = t.finishDate
        self.makeSpan = maxi

    def calcIndexCriticalPath(self):
        # Trouve les index des tâches sur le chemin critique
        # Input : Objet de type instance ou Tableau (JobID, taskID, start, fin, prédécesseur)
        # Output : Liste d'index
        if type(self) == Instance:
            task_list = sort_task(instance)
            task_list = np.array(task_list)
        if type(task_list) == list:
            task_list = np.array(task_list)

        for i, e in enumerate(task_list):
            if e[1][4] == 0:
                self.criticalPath.append(i)
