
class Resource:

    def __init__(self, name):
        self.state = "Free"
        self.name = name
        self.current_task = -1
        self.current_job = -1
        self.task_history = []

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

    def allocate(self, task):
        self.current_task = task
        self.current_job = task.job
        self.state = "Busy"
        self.task_history.append(self.current_task)

    def deallocate(self, task):
        self.current_task.job.next_task(self.current_task.taskID+1)
        self.current_task = -1
        self.current_job = -1
        self.state = "Free"
