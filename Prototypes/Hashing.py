import math
import time

class Hash_Table:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [[] for i in range(capacity)]
        self.keys = []

    def insert(self, key, value):
        index = self.hash_function(key)
        items = self.data[index]
        found = False
        for item in items:
            if item[0] == key:
                item[1] = value
                found = True
                break
        if not found:
            items.append([key, value])
            self.keys.append(key)

    def search(self, key):
        index = self.hash_function(key)
        items = self.data[index]
        if len(items) == 0 : return None
        if len(items) == 1 : return items[0][1]
        for item in items:
            if item[0] == key : return item[1]
        return None
    
    def hash_function(self, key):
        k = int(key.replace('-',''))
        x = k * 0.5*(math.sqrt(5) - 1) % 1
        return math.floor(self.capacity * x)

    def __setitem__(self, key, value):
        self.insert(key, value)

    def __getitem__(self, key):
        return self.search(key)
        
table = Hash_Table(100)
