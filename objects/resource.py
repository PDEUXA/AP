class Resource:

    def __init__(self, resource):
        self.state = "Free"
        self.name = resource
        self.current_task = -1
        self.current_job = 0

    def __str__(self):
        if self.current_task != -1:
            return 'Machine number = {0}, State = {1}, Current Job = {2}, Current Task = {3}'.format(
                self.name,
                self.state,
                self.current_task.jobID,
                self.current_task.taskID)
        else:
            return 'Machine number = {0}, State = {1}, Current Job = {2}, Current Task = {3}'.format(
                self.name,
                self.state,
                "N/A",
                "N/A")

    def update_current_task(self, task):
        self.current_task = task
        self.current_job = task.job
        self.state = "Busy"
