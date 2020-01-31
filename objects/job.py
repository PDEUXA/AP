from typing import List
from objects.task import Task


class Job:
    list_task: List[Task]

    def __init__(self, jobID, name, ressource):
        self.state = "Not Done"
        self.jobID = jobID
        self.job = name
        self.nb_task = int(len(self.job) / 2)
        self.list_task = []
        self.machine_per_task, self.duration_per_task = self.separate_jobs(self.job)
        for i, zipped in enumerate(zip(self.duration_per_task, self.machine_per_task)):
            self.list_task.append(Task(zipped[0], zipped[1], i, jobID, ressource[zipped[1]], self))
        self.current_task = self.list_task[0]

    def __str__(self):
        print('Task list')
        for i, task in enumerate(self.list_task):
            print("Task #", i, ":", task)
        return 'Job state= {0}'.format(self.state)

    def update_current_task(self, ongoingID, t):
        self.current_task = self.list_task[ongoingID]
        self.update_previous_task(self.current_task)
        self.current_task.allocate_to_ressource("On going", t)

    def update_previous_task(self,task):
        for tasks in self.list_task[:task.taskID]:
            tasks.update_task("Done")

    def next_task(self, ongoingID):
        if self.current_task.taskID + 1==len(self.list_task):
            self.update_previous_task(self.current_task)
            self.current_task.state = "Done"
            self.current_task = -1
            self.state = "Done"
        else:
            self.current_task = self.list_task[ongoingID]
            self.update_previous_task(self.current_task)

    @staticmethod
    def separate_jobs(j):
        machines = []
        durations = []
        for k, e in enumerate(j):
            if k % 2 == 0:
                # Machine
                machines.append(e)
            else:
                # Durée
                durations.append(e)
        return machines, durations
