import math
    
    
class Heap:                                                                     #MIN HEAP USED AS A PRIORITY QUEUE
    def __init__(self):                                                         
        self.array = [None]                                                     #ADD EMPTY ITEM SO INDEXING STARTS AT ONE
        
    def push(self, item):                                                       #ADD ITEM TO HEAP
        try : self.value(item)                                                  #MAKE SURE IT IS COMPATIBLE
        except : raise TypeError('New item not compatible with ordering function')
        self.array.append(item)
        self.array[self.length()].queue_index = self.length()                   #CHANGE INDEX OF ITEM SO IT CAN BE FOUND EASILY
        self.bubble_up(self.length())

    def pop(self):                                                              #REMOVE MIN ITEM
        if self.length() == 0 : raise IndexError('Queue is empty - cannot pop')
        item = self.array[1]
        self.array[1] = self.array[-1]
        self.array[1].queue_index = 1
        del self.array[-1]
        self.bubble_down(1)
        return item
    
    def update(self, index):                                                    #UPDATE THE POSITION OF AN ITEM
        self.bubble_up(index)                                                   #SCORE ONLY GOES DOWN SO BUBBLE UP

    def bubble_up(self, index):                                                 #COMPARE ITEM WITH PARENT AND SWAP UNTIL CORRECT
        while index//2 > 0:
            if self.compare(index//2, index) : break
            self.swap(index, index//2)
            index = index//2

    def bubble_down(self, index):                                               #COMPARE ITEM WITH CHILDREN AND SWAP UNTIL CORRECT
        while index*2+1 <= self.length():
            if self.compare(index*2, index*2+1, index):
                self.swap(index, index*2)
                index = index*2
            elif self.compare(index*2+1, index*2, index):
                self.swap(index, index*2+1)
                index = index*2+1
            else:
                break
        if index*2 <= self.length():                                            #IF ONLY HAS ONE CHILD COMPARE WITH THIS
            if self.compare(index*2, index):
                self.swap(index, index*2)

    def value(self, item):                                                      #GETS THE VALUE OF AN ITEM
        return item.score()
        
    def compare(self, a, b, c = None):                                          #COMPARES THE VALUE OF 2 OR 3 ITEMS
        try:
            if c == None:
                return self.value(self.array[a]) < self.value(self.array[b])
            return self.value(self.array[a]) <= self.value(self.array[b]) <= self.value(self.array[c])
        except:
            raise TypeError('Incomparable items in queue')

    def swap(self, a, b):                                                       #SWAP TWO ITEMS IN THE ARRAY
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp
        self.array[a].queue_index = a
        self.array[b].queue_index = b

    def length(self):                                                           #RETURNS LENGTH OF HEAP
        return len(self.array) - 1                                              #SUBTRACT ONE FOR EMPTY ITEM AT START
    


class Hash_Table:                                                               #HASH TABLE USED FOR STORING NODE DATA
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [[] for i in range(capacity)]                               #CREATE ARRAY OF SPECIFIC SIZE NEEDED
        self.keys = []

    def insert(self, key, value):
        try : index = self.hash_function(key)                                   #TEST THAT KEY IS COMPATIBLE WITH HASHING
        except : raise TypeError('Key incompatible with hash function')     
        items = self.data[index]
        found = False
        for item in items:                                                      #SEE IF ITEM HAS BEEN ADDED BEFORE
            if item[0] == key:
                item[1] = value                                                 #UPDATE VALUE INSTEAD OF ADDING IT AGAIN
                found = True
                break
        if not found : items.append([key, value])                               #ADD NEW VALUES
        self.keys.append(key)

    def search(self, key):                                                      #GET ITEM VIA KEY
        index = self.hash_function(key)
        items = self.data[index]
        for item in items:
            if item[0] == key : return item[1]                                  #LOOP THROUGH CHAINED ITEMS TO FIND SPECIFIC ONE
        return None
    
    def hash_function(self, key):                                               #APPLIES HASH FUNCTION TO KEY AND RETURNS OUTPUT
        k = int(key.replace('-',''))                                            #CONVERT ID TO A NUMBER
        x = k * 0.5 * (math.sqrt(5) - 1) % 1
        return math.floor(self.capacity * x)                                    #RETURN INTEGER VALUE

    def length(self):                                                           #RETURN LENGTH OF HASH TABLE
        return self.capacity

    def __setitem__(self, key, value):                                          #IN-BUILT FUNCTIONALITY TO ADD ITEM VIA []
        self.insert(key, value)

    def __getitem__(self, key):                                                 #IN-BUILT FUNCTIONALITY TO FIND ITEM VIA []                                               
        return self.search(key)
