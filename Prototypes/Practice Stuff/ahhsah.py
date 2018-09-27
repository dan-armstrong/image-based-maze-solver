class Hash:                                                                     #HASH TABLE CLASS
    def __init__(self, size):
        self.size = size                                                        #SET CAPACITY
        self.table = []
        for i in self.size : self.table.append([])

    def index(self, key):                                                       #HASH FUNCTION
        value = int(key.replace('-',''))
        frac = value * 0.5 * (math.sqrt(5) - 1) % 1
        return math.floor(self.size * frac)
    
    def __setitem__(self, key, value):                                          #ADD ITEM TO TABLE
        index = self.index(key)
        items = self.data[index]
        items.append([key, value])

    def __getitem__(self, key):                                                 #GET ITEM BY KEY
        index = self.hash_function(key)
        items = self.data[index]
        for item in items:
            if item[0] == key : return item[1]
        return None
