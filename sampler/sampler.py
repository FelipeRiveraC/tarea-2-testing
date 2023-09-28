from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames


class Tree:

    def __init__(self, name):
        self.name = name
        self.root: Node = Node(name)
    
    def updateTimes(self, trace: list[str]=None):
        self.root.updateTimes(trace)
        

    def addChild(self, trace: list[str]):
        node = self.root
        for name in trace:
            if len(list(filter(lambda x: x.name == name, node.children))) > 0:
                node = list(filter(lambda x: x.name == name, node.children))[0]
            else:
                newNode = Node(name, node)
                node.children.append(newNode)
                node = newNode
                

    def __str__(self):
        return str(self.root)
        

    
class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.times = 0
        self.parent = parent
        self.children: list[Node] = []

    def updateTimes(self, trace: list[str]=None):     
        #  for times to run it needs to be on trace or name total

        if self.name not in trace and self.name != "total":
            return
        self.times += 1
        
        for child in self.children:
            child.updateTimes(trace)

        

    def depth(self):
        
        depth = 0
        current = self
        while current.parent:
            depth += 1
            current = current.parent
        return depth

    def __str__(self):
        tabs = '  ' * self.depth()
        
        children_str = "".join(map(str, self.children))
        return tabs + self.name + " (" + str(self.times) + " seconds)\n" + children_str
    

class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.trace = Tree("total")
        
        
    def start(self):
        self.active = True
        self.t.start()

    
    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                self.trace.addChild(stack)
        
        self.trace.updateTimes(stack)
    
    def sample(self):
        while self.active:
            self.checkTrace()
            
            sleep(1)

    def printReport(self):
        # Este metodo debe imprimir el reporte del call context tree
        print(self.trace)
        
        
