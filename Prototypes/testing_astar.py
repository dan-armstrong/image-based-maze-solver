import csv
from PIL import Image as PIL

def display_ordered_nodes():
    node_grid = csv.open_integer_grid('nodes_display.csv')
    file = open('nodes_visited.txt', 'r')
    total = int(file.read())
    file.close()
    img = PIL.new('RGB',(len(node_grid[0]),len(node_grid)))
    pixels = img.load()
    for y in range(len(node_grid)):
        for x in range(len(node_grid[y])):
            if node_grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            elif node_grid[y][x] == 1:
                pixels[x,y] = (0,0,0)
            else:
                colour = round(255 * node_grid[y][x] / total)
                pixels[x,y] = (colour,0,255-colour)
    return img

display_ordered_nodes().show()
display_ordered_nodes().save('nodesmaprings.png')
