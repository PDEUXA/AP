from typing import List
from objects.task import Task


class Job:
    list_task: List[Task]

    def __init__(self, jobID, job, ressource):
        self.state = "Not Done"
        self.jobID = jobID
        self.job = job
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

    def update_current_task(self, ongoingID):
        self.current_task = self.list_task[ongoingID]

    def update_all_task(self):
        for task in reversed(self.list_task):
            if task.state == "On going":
                ongoingID = task.taskID
                self.update_current_task(ongoingID)
            elif task.state == "Not Started":
                pass
            elif task.state == "On going":
                if task.taskID < ongoingID:
                    task.update_task("Done")
                else:
                    task.update_task("Not Started")

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
