import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Stack:
    def __init__(self): 
        self._data=[]
        
    def push(self, item): 
        self._data.append(item)
        
    def pop(self):
        if not self._data: raise IndexError("Stack is empty")
        return self._data.pop()
        
    def is_empty(self): 
        return len(self._data)==0
