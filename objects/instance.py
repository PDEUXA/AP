from objects.job import Job
from objects.resource import Resource


class Instance:
    def __init__(self, **attributes):
        for attr_name, attr_value in attributes.items():
            setattr(self, attr_name, attr_value)
        # self.nb_machine = nb_machine
        # self.nb_jobs = nb_jobs
        # self.problem = problem
        self.resource_list = []
        self.jobs_list = []
        self.makeSpan = -1

        # Create Resources
        for i in range(self.nb_machine):
            self.resource_list.append(Resource(i))
        # Create jobs
        for i in range(self.nb_jobs):
            self.jobs_list.append(Job(i, self.problem[i], self.resource_list, self))

    def __str__(self):
        return '{}'.format(self.problem)

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
