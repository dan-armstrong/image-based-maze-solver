from PIL import Image

def readCSV(fileName):
    file = open(fileName, 'r')
    grid = []
    for line in file:
        grid.append([])
        for n in line.split(','):
            grid[-1].append(int(n))
    return grid

def drawPath(grid, path):
    prev = None
    for point in path:
        grid[point[1]][point[0]] = 2
        if prev != None:
            for x in range(prev[0],point[0]):
                grid[point[1]][x] = 2
            for x in range(point[0],prev[0]):
                grid[point[1]][x] = 2
            for y in range(prev[1],point[1]):
                grid[y][point[0]] = 2
            for y in range(point[1],prev[1]):
                grid[y][point[0]] = 2
        prev = point
    return grid

def displayGrid(grid):
    image = Image.new('RGB',(len(grid[0]),len(grid)))
    pixels = image.load()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            if grid[y][x] == 1:
                pixels[x,y] = (0,0,0)
            if grid[y][x] == 2:
                pixels[x,y] = (255,0,255)
            if grid[y][x] == 3:
                pixels[x,y] = (0,0,255)
    image.show()
