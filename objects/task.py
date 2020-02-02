from objects.resource import Resource


class Task:
    machine: Resource

    def __init__(self, duration, machine, taskID, jobID, ressource, job):
        self.state = "Not Started"
        self.startDate = "N/A"
        self.duration = duration
        self.finishDate = "N/A"
        self.machine = ressource
        self.job = job
        self.machineID = machine
        self.taskID = taskID
        self.jobID = jobID
        self.startSucessor = -1

    def __str__(self):
        return 'JobID= {0}, taskID= {1}, Start= {2}, Finish={3}, Machine= {4}, State= {5}'.format(self.jobID,
                                                                                                  self.taskID,
                                                                                                  self.startDate,
                                                                                                  self.finishDate,
                                                                                                  self.machine.name,
                                                                                                  self.state)

    def update_task(self, state):
        self.state = state

    def allocate_to_ressource(self, state, t):
        self.update_task(state)
        self.startDate = t
        self.finishDate = self.startDate + self.duration
        self.machine.allocate(self)

    def deallocate_to_ressource(self, state):
        self.update_task(state)
        self.machine.deallocate(self)
