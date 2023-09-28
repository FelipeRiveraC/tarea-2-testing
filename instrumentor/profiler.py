import time
from function_record import *
from abstract_profiler import AbstractProfiler
import pdb


class Profiler(AbstractProfiler):

    def __init__(self):
        self.records = {}
        self.queue = []
    
    # search a record by name
    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    # metodo se llama cada vez que se ejecuta una funcion    
    def fun_call_start(self, functionName, args):
        record = self.get_record(functionName)


        function_object = self.records[functionName]
        function_object.enter_queue_cache(args)

        for record in self.records.values():
            if len(self.queue) and self.queue[-1].functionName == record.functionName:
                function_object.callers.append(record.functionName)
        
        self.queue.append(function_object)
        
        function_object.frecuency += 1
        function_object.start_time = time.time()
        
       
    def fun_call_end(self, functionName, returnValue):
        function_object = self.records[functionName]
        function_object.end_time = time.time()
        function_object.calculate_execution_time()
        function_object.leave_queue_cache(returnValue)
        
        self.queue.pop()
    
    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


