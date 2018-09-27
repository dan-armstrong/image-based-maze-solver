import csv
from PIL import Image as PIL

def display_rectangles():
    maze_grid = csv.open_integer_grid('maze.csv')
    rect_grid = csv.open_integer_grid('rectangles.csv')
    img = PIL.new('RGB',(len(maze_grid[0]),len(maze_grid)))
    pixels = img.load()
    nodes = 0
    removed = 0
    for y in range(len(maze_grid)):
        for x in range(len(maze_grid[y])):
            if rect_grid[y][x] == 1:
                nodes += 1
                pixels[x,y] = (255,0,255)
            elif rect_grid[y][x] == 2:
                removed += 1
                pixels[x,y] = (255,255,255)
            elif maze_grid[y][x] == 0:
                nodes += 1
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)
    print(round(removed/(nodes+removed)*100, 2), 'percent of nodes removed by RSR')
    return img

def display_nodes():
    maze_grid = csv.open_integer_grid('maze.csv')
    nodes_grid = csv.open_integer_grid('nodes.csv')
    img = PIL.new('RGB',(len(maze_grid[0]),len(maze_grid)))
    pixels = img.load()
    for y in range(len(maze_grid)):
        for x in range(len(maze_grid[y])):
            if maze_grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)
    for node in nodes_grid:
        pixels[node[0], node[1]] = (255,0,255)
    return img

def display_walls():
    walls_grid = csv.open_integer_grid('walls.csv')
    vertical_walls = []
    horizontal_walls = []
    for data in walls_grid:
        vertical_walls.append(data[0])
        horizontal_walls.append(data[1])
    img = PIL.open()
    pixels = img.load()
    for x in vertical_walls:
        
    or y in horizontal_walls:
                pixels[x,y] = (255,0,255)
            elif maze_grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            else:
                pixels[x,y] = (0,0,0)
    return img


display_walls().show()
