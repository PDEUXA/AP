from objects.resource import Resource


class Task:
    machine: Resource

    def __init__(self, duration, machine, taskID, jobID, ressource, job):
        self.state = "Not Started"
        self.startDate = 0
        self.duration = duration
        self.finishDate = duration
        self.machine = ressource
        self.job = job
        self.machineID = machine
        self.taskID = taskID
        self.jobID = jobID

    def __str__(self):
        return 'JobID= {0}, taskID= {1}, Start= {2}, Finish={3}, Machine= {4}, State= {5}'.format(self.jobID,
                                                                                                  self.taskID,
                                                                                                  self.startDate,
                                                                                                  self.finishDate,
                                                                                                  self.machine,
                                                                                                  self.state)

    def update_task(self, state):
        self.state = state

    def update_task_and_date(self, state, t):
        self.state = state
        self.startDate = t
        self.finishDate = self.startDate + self.duration
