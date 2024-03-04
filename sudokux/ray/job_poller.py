import ray
from sudokux.solver.utils import *

@ray.remote
class JobPuller:
    def __init__(self, np_list) -> None:
        self.current=0
        self.np_list=np_list
    
    def pull(self):
        if self.current>=len(self.np_list):
            return ""
        else:
            return self.np_list['puzzle'][self.current]