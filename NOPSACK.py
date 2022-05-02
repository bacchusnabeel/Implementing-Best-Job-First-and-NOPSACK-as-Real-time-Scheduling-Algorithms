"""
NOPSACK based on 0-1 Knapsack algorithm for uniprocessor architectures.
"""
from simso.core import Scheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.NOPSACK", 
    required_task_fields = [
        {'name': 'priority', 'type' : 'int', 'default' : '0' } 
    ]
)

class NOPSACK(Scheduler):
    def init(self):
        self.ready_list = []
        self.bag = []
        self.capacity = 0

    def on_activate(self, job):
        # job.ratio = 0
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        # self.bag.remove(job)
        self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        if len(self.bag) > 0:
            job = max(self.bag, key = lambda x: x.ratio)
            self.bag.remove(job)
            
        elif len(self.ready_list) > 0:
            # Calculate the ratio for each job
            total_cost = 0
            templist= []
            for x in self.ready_list:
                total_cost += x.wcet
                x.ratio = (x.data['priority']/x.laxity)+1
                templist.append(x)
            # Calculate the bag capacity
            self.capacity = total_cost/len(self.ready_list)

            # # Insert jobs into the bag until capacity is filled
            while self.capacity >= 0 and len(templist) > 0:
                job = max(templist, key = lambda x: x.ratio)
                self.capacity -= job.wcet
                self.bag.append(job)
                templist.remove(job)

            # job with the highest ratio
            job = max(self.bag, key = lambda x: x.ratio)
            self.bag.remove(job)
        else:
            job = None

        return (job, cpu)