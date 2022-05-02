"""
Best Job First algorithm for uniprocessor architectures.
"""
from simso.core import Scheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.BJF", 
    required_task_fields = [
        {'name': 'priority', 'type' : 'int', 'default' : '0' }   
    ]
)

class BJF(Scheduler):
    def init(self):
        self.ready_list = []
        self.EDF_weight = 0.2
        self.LLF_weight = 0.2
        self.P_weight = 0.6

    def on_activate(self, job):
        job.f = 0
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if self.ready_list:
            # job with the factor f

            for x in self.ready_list:
                x.f = x.absolute_deadline * self.EDF_weight + x.laxity * self.LLF_weight + x.data['priority'] * self.P_weight

            job = min(self.ready_list, key=lambda x: x.f)
        else:
            job = None

        return (job, cpu)