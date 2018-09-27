                                                                                                                                                #OUT OF BOUNDS
from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS ORIGINAL NAME USED FOR CLASS
import subprocess

class Image:                                                                    #IMAGE CLASS THAT STORES DATA ABOUT AN INDIVIDUAL IMAGE
    def __init__(self, fileName):
        self.data = PIL.open(fileName)                                          #STORES IMAGE DATA AS A PIL OBJECT
        self.dimensions = [self.data.size[0], self.data.size[1]]                #STORES DIMENSIONS [WIDTH, HEIGHT]
    
    def rgb(self):                                                              #CONVERTS IMAGE DATA INTO RGB GRID
        rgb_data = self.data.convert('RGB')                                     
        pixels = rgb_data.load()                                                
        grid = []                                                               #THREE-DIMENSIONAL LIST OF RGB VALUES
        for y in range(self.dimensions[1]):                                     #LOOP THROUGH IMAGE ROWS
            grid.append([])                                                     
            for x in range(self.dimensions[0]):                                 #LOOP THROUGH PIXELS IN ROW
                grid[y].append(list(pixels[x,y]))                               #[R,G,B] VALUE REPRESENTS THE CORRESPONDING PIXEL
        return grid                                                             #RETURNS AN RGB GRID AS A THREE-DIMENSIONAL INT LIST

    def greyscale(self):                                                        #CONVERTS RGB GRID INTO GREYSCALE GRID                                                       
        rgb_grid = self.rgb()
        greyscale_grid = []                                                     #TWO-DIMENSIONAL LIST OF LUMINANCE VALUES
        for y in range(self.dimensions[1]):                                     #LOOP THROUGH IMAGE ROWS 
            greyscale_grid.append([])                                                     
            for x in range(self.dimensions[0]):                                 #LOOP THROUGH PIXELS IN ROW
                r_luminance = rgb_grid[y][x][0]*0.2126                          #CALCULATE LUMINANCE VALUES FOR EACH COLOUR OF THE PIXEL
                g_luminance = rgb_grid[y][x][1]*0.7152
                b_luminance = rgb_grid[y][x][2]*0.0722
                luminance = round(r_luminance + g_luminance + b_luminance)      #ROUNDED SUM OF INDIVIDUAL LUMINANCES
                greyscale_grid[y].append(luminance)                             #LUMINANCE VALUE REPRESENTS THE CORRESPONDING PIXEL
        return greyscale_grid                                                   #RETURNS GREYSCALE GRID AS A TWO-DIMENSIONAL INT LIST

    def histogram(self):                                                        #CREATES HISTOGRAM OF GREYSCALE PIXEL COLOUR FREQUENCIES
        grid = self.greyscale()
        hist = [0] * 256                                                        #CREATE LIST FOR ALL POSSIBLE GREYSCALE VALUES (0 TO 255)                          
        for y in range(len(grid)):                                              #LOOP THROUGH ROWS OF GRID
            for x in range(len(grid[y])):                                       #LOOP THROUGH GREYSCALE VALUES IN ROW
                hist[grid[y][x]] += 1                                            
        return hist                                                             #RETURNS HISTOGRAM OF GREYSCALE PIXEL AMOUNTS AS AN INT LIST

    def threshold_value(self, hist):#DO IN R maybe
        mean_values = []
        class_variances = []
        for i in range(len(hist)):
            mean_values.append(i*hist[i])
        
        for t in range(len(hist)+1):
            weight_bg = sum(hist[:t])/(self.dimensions[0]*self.dimensions[1])
            weight_fg = sum(hist[t:])/(self.dimensions[0]*self.dimensions[1])
            if sum(hist[:t]) == 0:
                mean_bg = 0
            else:
                mean_bg = sum(mean_values[:t])/sum(hist[:t])
            if sum(hist[t:]) == 0:
                mean_fg = 0
            else:
                mean_fg = sum(mean_values[t:])/sum(hist[t:])
            class_variances.append(weight_bg*weight_fg*(mean_bg-mean_fg)**2)
        return class_variances.index(max(class_variances))
        

    def threshold(self):
        grid = self.greyscale()
        hist = self.histogram()
        t = self.threshold_value(hist)

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] > t:
                    grid[y][x] = 1
                else:
                    grid[y][x] = 0
        return grid

    def csv(self, grid):
        csv_string = ''
        for row in grid:
            for item in row:
                csv += str(item).replace(', ', ' - ').replace('[','').replace(']','') + ','
            csv = csv[:-1] + '\n'
        return csv[:-1]
                
    def crop(self):
        grid = self.threshold()
        csv_path = '/Users/danarmstrong/Desktop/Coursework/threshold.csv'
        cmd_path = '/usr/local/bin/Rscript'
        script_path = '/Users/danarmstrong/Desktop/Coursework/crop_image.r'

        file = open(csvPath, 'w')
        file.write(threshold)
        file.close()
        
        subprocess.check_output([cmd_path, script_path, csv_path], universal_newlines=True)
        
        
    def display(self, grid):
        display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
        pixels = display_image.load()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                pixels[x,y] = (grid[y][x]*255,grid[y][x]*255,grid[y][x]*255)
        display_image.show()


class Node:
    def __init__(self, cost, heuristic, name):
        self.cost = cost
        self.heuristic = heuristic
        self.id = name
    def score(self):
        return self.cost + self.heuristic

                                                                                                                                                #OUT OF BOUNDS
class Priority_Queue:                                                           #PRIORITY QUEUE THAT STORES UNVISITED NODES                                                           
    def __init__(self):                                                         
        self.queue = []                                                         #QUEUE REPRESENTED AS AN ORDERED LIST

    def value(self, index):                                                     #CALCULATES SCORE OF NODE AT CERTAIN INDEX IN QUEUE
        return self.queue[index].score()                                        #RETURNS SCORE OF NODE

    def length(self):                                                           #CALCULATES LENGTH OF QUEUE
        return len(self.queue)                                                  #RETURNS LENGTH OF QUEUE

    def pop(self):                                                              #POPS FIRST ITEM OFF THE QUEUE
        item = self.queue[0]                                                
        self.queue.pop(0)                                                       #REMOVE FIRST ITEM
        return item                                                             #RETURN THIS ITEM

    def find(self, item):                                                       #FINDS POSITION OF NODE IN QUEUE VIA BINARY SEARCH
        search = self.order_attribute(item)                                     #QUEUE ORDERED BY NODE SCORES NOT NODE ITSELF
        minimum = 0                                                             #BINARY SEARCH TO FIND POSITION OF NODE WITH SAME SCORE
        maximum = self.length()-1
        current = maximum//2
        
        while self.value(current) != search and minimum != maximum:             
            if self.value(current) < search:
                minimum = min(current + 1, maximum)
            elif self.value(current) > search:
                maximum = max(current - 1, minimum)
            current = (minimum + maximum)//2

        if self.value(current) == search:                                       #MULTIPLE NODES MAY HAVE SAME F(N) SO NEED TO SEARCH FURTHER
            if item == self.queue[current] : return current                     #RETURN CURRENT INDEX IF NODE IS THERE 
            minumum = current-1
            maximum = curent+1
            while search == self.value(minimum) and minumum >= 0:               #SEARCH BACKWARDS THROUGH NODES WITH SAME F(N) TO START
                if item == self.queue[minumum] : return minumum                 #RETURN MINIMUM INDEX IF NODE IS THERE
                minumum -= 1
            while search == self.value(maximum) and maximum <= self.length()-1: #SEARCH FORWARDS THROUGH NODES WITH SAME F(N) TO END
                if item == self.queue[maximum] : return maximum                 #RETURN MAXIMUM INDEX IF NODE IS THERE
                maximum += 1
        return None                                                             #RETURN NONE IF NODE NOT FOUND
        
    def push(self, item):                                                       #ADDS ITEM TO ORDERED QUEUE IN CORRECT POSITION
        if self.length() == 0:                                                  #CHECKS IF QUEUE IS EMPTY
            self.queue = [item]                                                 #ADD ITEM AS FIRST ELEMENT OF QUEUE
        else:                                                                   #BINARY SEARCH USED TO FIND QUEUE POSITION
            search = self.order_attribute(item)                                 #QUEUE ORDERED BY NODE SCORES NOT NODE ITSELF
            minimum = 0
            maximum = len(self.queue)-1
            current = maximum//2
            
            while self.value(current) != search and minimum != maximum:         #BINARY SEARCH TO FIND INSERTION POSITION
                if self.value(current) < search:
                    minimum = min(current + 1, maximum)
                elif self.value(current) > search:
                    maximum = max(current - 1, minimum)
                current = (minimum + maximum)//2

            if self.value(current) == search:                                   #IF NODES WITH SAME SCORE IN QUEUE ALREADY
                while search == self.value(current-1) and current > 0:          #INSERT NEW NODE BEFORE ALL OTHERS WITH THE SAME VALUE
                    current -= 1
                self.queue.insert(current,item)
            else:                                                               #IF NDOE'S SCORE NOT IN QUEUE
                if search < self.value(current):                                #INSERT NEW NODE BEFORE IF SCORE LESS THAN CURRENT NODE
                    self.queue.insert(current,item)
                else:                                                           #INSERT NEW NODE AFTER IF SCORE MORE THAN CURRENT NODE
                    self.queue.insert(current+1,item)

    def update(self, item):
        print(1)
    def display(self):
        display_list = []
        for node in self.queue:
            display_list.append(node.id + ' ' + str(node.cost) + ' ' + str(node.heuristic) + ' ' + str(self.value(self.queue.index(node))))
        print(display_list)


f = lambda x: x.cost + x.heuristic
a = Priority_Queue(f)
for i in range(10):
    a.push(Node(round(i**i**0.5%10), round(i**2), str(i)))
x = Node(6,2,'d')
a.push(x)
a.display()
print(a.find(x))
