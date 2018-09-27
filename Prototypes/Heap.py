class Heap:
    def __init__(self):
        self.array = [None]

    def push(self, item):
        self.array.append(item)
        index = self.length()
        while index//2 > 0:
            if self.array[index] < self.array[index//2] : break
            self.swap(index, index//2)
            index = index//2

    def pop(self):
        if self.length() == 0 : return None
        item = self.array[1]
        self.array[1] = self.array[-1]
        del self.array[-1]

        index = 1
        while index*2+1 <= self.length():
            if self.array[index*2] > self.array[index*2+1] > self.array[index]:
                self.swap(index, index*2)
                index = index*2
            elif self.array[index*2+1] > self.array[index*2] > self.array[index]:
                self.swap(index, index*2+1)
                index = index*2+1
            else:
                break

        if index*2 <= self.length():
            if self.array[index*2] > self.array[index]:
                self.swap(index, index*2)
        return item
    
    def swap(self, a, b):
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp

    def length(self):
        return len(self.array) - 1

class Heap2:
    def __init__(self, function):
        self.array = [None]
        self.value = function
        
    def push(self, item):
        self.array.append(item)
        self.bubble_up(self.length())

    def pop(self):
        if self.length() == 0 : return None
        item = self.array[1]
        self.array[1] = self.array[-1]
        del self.array[-1]
        self.bubble_down(1)
        return item

    def update(self, index, item):
        self.array[index] = item
        self.bubble_up(index)
        self.bubble_down(index)

    def bubble_up(self, index):
        while index//2 > 0:
            if self.compare(index//2, index) : break
            self.swap(index, index//2)
            index = index//2

    def bubble_down(self, index):
        while index*2+1 <= self.length():
            if self.compare(index*2, index*2+1, index):
                self.swap(index, index*2)
                index = index*2
            elif self.compare(index*2+1, index*2, index):
                self.swap(index, index*2+1)
                index = index*2+1
            else:
                break
        if index*2 <= self.length():
            if self.compare(index*2, index):
                self.swap(index, index*2)

    def compare(self, a, b, c = None):
        if c == None:
            return self.value(self.array[a]) > self.value(self.array[b])
        return self.value(self.array[a]) > self.value(self.array[b]) > self.value(self.array[c])
        
    def swap(self, a, b):
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp

    def length(self):
        return len(self.array) - 1

