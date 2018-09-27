from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS SIMILAR NAME USED FOR THIS FILE
import subprocess
import math
import time

def data(file_name):                                                            #OPENS IMAGE FILE 
    return PIL.open(file_name)                                                  #RETURNS IMAGE DATA AS A PIL OBJECT


def greyscale(img_data):                                                        #CONVERTS RGB GRID INTO GREYSCALE GRID                                                       
    rgb_data = img_data.convert('RGB')
    pixels = rgb_data.load()
    grey_grid = []                                                              #TWO-DIMENSIONAL LIST OF LUMINANCE VALUES
    for y in range(img_data.size[1]):                                              #LOOP THROUGH IMAGE ROWS 
        grey_grid.append([])                                                     
        for x in range(img_data.size[0]):                                       #LOOP THROUGH PIXELS IN ROW
            r_luminance = pixels[x,y][0]*0.2126                              #CALCULATE LUMINANCE VALUES FOR EACH COLOUR OF THE PIXEL
            g_luminance = pixels[x,y][1]*0.7152
            b_luminance = pixels[x,y][2]*0.0722
            luminance = round(r_luminance + g_luminance + b_luminance)          #ROUNDED SUM OF INDIVIDUAL LUMINANCES
            grey_grid[y].append(luminance)                                      #LUMINANCE VALUE REPRESENTS THE CORRESPONDING PIXEL
    return grey_grid                                                            #RETURNS GREYSCALE GRID AS A TWO-DIMENSIONAL INT LIST


def save_csv(grid, name):
    csv_string = ''
    for row in grid:
        csv_string += str(row)[1:-1].replace(' ','') + '\n'
    file = open(name, 'w')
    file.write(csv_string[:-1])
    file.close()


def open_csv(name):
    file = open(name, 'r')
    csv = file.read()
    file.close()
    csv_rows = csv.split('\n')
    grid = []
    for csv_row in csv_rows:
        grid_row = []
        csv_row = csv_row.split(',')
        for item in csv_row:
            try : grid_row.append(int(item))
            except : pass
        if len(grid_row) > 0 : grid.append(grid_row)
    return grid

    
def display(grid):
    display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
    pixels = display_image.load()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if type(grid[y][x]) == int:
                pixels[x,y] = (grid[y][x], grid[y][x], grid[y][x])
            else:
                pixels[x,y] = (grid[y][x][0], grid[y][x][1], grid[y][x][2])
    display_image.show()


def display_threshold(grid):
    display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
    pixels = display_image.load()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            elif grid[y][x] == 1:
                pixels[x,y] = (0,0,0)
            elif grid[y][x] == 2:
                pixels[x,y] = (255,0,255)
            elif grid[y][x] == 3:
                pixels[x,y] = (0,255,255)
            elif grid[y][x] == 4:
                pixels[x,y] = (0,0,255)
            elif grid[y][x] == 5:
                pixels[x,y] = (255,0,0)
    display_image.show()


def display_path(grid,path):
    display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
    pixels = display_image.load()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            elif grid[y][x] == 1:
                pixels[x,y] = (0,0,0)
    for p in path:
        pixels[p[0],p[1]] = (255,0,255)
    display_image.show()

