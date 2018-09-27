from PIL import Image
import subprocess

class Maze_Image:
    def __init__(self, fileName):
        self.address = fileName
        self.data = Image.open(self.address)
        self.dimensions = [self.data.size[0], self.data.size[1]]
        self.rgb_grid = self.rgb()

    def rgb(self):
        rgb_data = self.data.convert('RGB')
        pixels = rgb_data.load()
        grid = []
        for y in range(self.dimensions[1]):
            grid.append([])
            for x in range(self.dimensions[0]):
                grid[y].append(list(pixels[x,y]))
        return grid

    def greyscale(self):
        grid = []
        for y in range(self.dimensions[1]):
            grid.append([])
            for x in range(self.dimensions[0]):
                grid[y].append((self.rgb_grid[y][x][0]*0.2126 + self.rgb_grid[y][x][1]*0.7152 + self.rgb_grid[y][x][2]*0.0722))
        return grid

    def histogram(self):
        grid = self.greyscale()
        hist = [0] * 256
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                hist[int(round(grid[y][x]))] += 1
        return hist

    def display_greyscale(self):
        grid = self.threshold()
        image = Image.new('RGB',(len(grid[0]),len(grid)))
        pixels = image.load()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                pixels[x,y] = (round(grid[y][x]*255),round(grid[y][x]*255),round(grid[y][x]*255))
        image.show()

    def threshold(self):
        hist = self.histogram()
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
        threshold_value = class_variances.index(max(class_variances))

        grid = self.greyscale()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] > threshold_value:
                    grid[y][x] = 1
                else:
                    grid[y][x] = 0
        return grid
        
            
a = Maze_Image('/Users/danarmstrong/Desktop/test.jpg')
a.display_greyscale()
