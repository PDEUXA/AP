from objects.resource import Resource


class Task:
    machine: Resource

    def __init__(self, duration, machine, taskID, jobID, ressource, job):
        self.state = "Not Started"
        self.startDate = 10000
        self.duration = duration
        self.finishDate = 10000
        self.machine = ressource
        self.job = job
        self.machineID = machine
        self.taskID = taskID
        self.jobID = jobID

        self.startSucessor = -1
        self.freeFloat = -1
        self.totalFloat = -1
        self.critical = False

    def __str__(self):
        return 'JobID= {0}, taskID= {1}, Start= {2}, Finish={3}, Duration={4}, Machine= {5}, State= {6}'.format(
            self.jobID,
            self.taskID,
            self.startDate,
            self.finishDate,
            self.duration,
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

    def isCritical(self):
        if self.totalFloat == 0:
            self.critical = True

    def setFreeFloat(self, value):
        self.freeFloat = value

    def setTotalFloat(self, value):
        self.totalFloat = value

    def setStartSucessor(self, value):
        self.startSucessor = value
