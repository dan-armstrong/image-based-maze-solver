from PIL import Image
import time
import subprocess
import find_path

COMMAND_PATH = '/usr/local/bin/Rscript'
SCRIPT_PATH = '/Users/danarmstrong/Documents/School/Computing/Coursework/find_nodes.r'
IMAGE_PATH = '/Users/danarmstrong/Downloads/maze.png'
CSV_PATH = '/Users/danarmstrong/Documents/School/Computing/Coursework/image_data.csv'

def createThreshold(imageName):
    image = Image.open(imageName).convert('RGB')
    sizeX = image.size[0]
    sizeY = image.size[1]
    pixels = image.load() #PIXEL DATA
    threshold = ''

    for y in range(0,sizeY): #CREATE THRESHOLD GRID FROM IMAGE
        for x in range(0,sizeX):
            if sum(pixels[x,y]) < 255*3*0.5: #IF PIXEL IS DARK
                threshold += '1,'
            else:
                threshold += '0,'
        threshold = threshold[:-1] + '\n'
    return threshold

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

threshold = createThreshold(IMAGE_PATH)
file = open(CSV_PATH, 'w')
file.write(threshold)
file.close()

nodeData = subprocess.check_output([COMMAND_PATH, SCRIPT_PATH, CSV_PATH], universal_newlines=True).split('\n')

grid = readCSV('test.csv')
displayGrid(grid)
grid = readCSV(CSV_PATH)
displayGrid(grid)
path = pathfinder.findPath(nodeData)
grid = drawPath(grid, path)
displayGrid(grid)
