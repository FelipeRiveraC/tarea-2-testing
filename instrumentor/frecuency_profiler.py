from profiler import Profiler

class FrecuencyProfiler(Profiler):
    
    def __init__(self):
        super().__init__()

    def fun_call_start(self, functionName, args):
        if functionName not in self.records:
            self.records[functionName] = 1
        else:
            self.records[functionName] += 1