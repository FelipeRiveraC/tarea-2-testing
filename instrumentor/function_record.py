import pdb

class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.frecuency = 0
        self.start_time = 0
        self.end_time = 0
        self.times = []
        self.callers = []
        self.cache_info = []
        self.final_cache = []

    def calculate_execution_time(self):
        time = self.end_time - self.start_time
        self.times += [time]
        self.start_time = 0
        # pdb.set_trace()
        self.end_time = 0
        return time
    
    def enter_queue_cache(self, args):
        self.cache_info.append({
            "arguments": args,
            "return_value": None
        })

    def leave_queue_cache(self, returnValue):
        item = self.cache_info.pop()
        item["return_value"] = str(returnValue)
        self.final_cache.append(item)
    
    def get_avg_time(self):
        if len(self.times) == 0: return 0

        return sum(self.times) / len(self.times)
    
    def get_max_time(self):
        if len(self.times) == 0: return 0

        return max(self.times)
    
    def get_min_time(self):

        if len(self.times) == 0: return 0

        return min(self.times)
    
    def find_cache_candidates(self):
        groupedCalls = {}
        for call in self.final_cache:
            arg_key = str(call["arguments"])
            if arg_key not in groupedCalls:
                groupedCalls[arg_key] = [call["return_value"]]
            else:
                groupedCalls[arg_key].append(call["return_value"])
        
        for arg, return_values in groupedCalls.items():
            #pdb.set_trace()
            unique_return_values = set(return_values)
            if len(unique_return_values) == 1:
                # Same arguments with consistent return value and occurred more than once
                return 1
        return 0


    def print_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
            self.functionName,
            self.frecuency,
            self.get_avg_time(), 
            self.get_max_time(),
            self.get_min_time(), self.find_cache_candidates(), "[" + ", ".join(self.callers) + "]"))
