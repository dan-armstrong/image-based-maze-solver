from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS SIMILAR NAME USED FOR THIS FILE
import subprocess
import math


def data(file_name):                                                            #OPENS IMAGE FILE 
    return PIL.open(file_name)                                                  #RETURNS IMAGE DATA AS A PIL OBJECT


def dimensions(data):                                                           #FINDS THE SIZE OF AN IMAGE
    return [data.size[0], data.size[1]]                                         #RETURNS DIMENSIONS [WIDTH, HEIGHT]


def rgb(data):                                                                  #CONVERTS IMAGE DATA INTO RGB GRID
    rgb_data = data.convert('RGB')                                     
    pixels = rgb_data.load()
    width = dimensions(data)[0]
    height = dimensions(data)[1]
    grid = []                                                                   #THREE-DIMENSIONAL LIST OF RGB VALUES
    for y in range(height):                                                     #LOOP THROUGH IMAGE ROWS
        grid.append([])                                                     
        for x in range(width):                                                  #LOOP THROUGH PIXELS IN ROW
            grid[y].append(list(pixels[x,y]))                                   #[R,G,B] VALUE REPRESENTS THE CORRESPONDING PIXEL
    return grid                                                                 #RETURNS AN RGB GRID AS A THREE-DIMENSIONAL INT LIST

def greyscale(rgb_grid):                                                        #CONVERTS RGB GRID INTO GREYSCALE GRID                                                       
    grey_grid = []                                                              #TWO-DIMENSIONAL LIST OF LUMINANCE VALUES
    for y in range(len(rgb_grid)):                                              #LOOP THROUGH IMAGE ROWS 
        grey_grid.append([])                                                     
        for x in range(len(rgb_grid[y])):                                       #LOOP THROUGH PIXELS IN ROW
            r_luminance = rgb_grid[y][x][0]*0.2126                              #CALCULATE LUMINANCE VALUES FOR EACH COLOUR OF THE PIXEL
            g_luminance = rgb_grid[y][x][1]*0.7152
            b_luminance = rgb_grid[y][x][2]*0.0722
            luminance = round(r_luminance + g_luminance + b_luminance)          #ROUNDED SUM OF INDIVIDUAL LUMINANCES
            grey_grid[y].append(luminance)                                      #LUMINANCE VALUE REPRESENTS THE CORRESPONDING PIXEL
    return grey_grid                                                            #RETURNS GREYSCALE GRID AS A TWO-DIMENSIONAL INT LIST


def histogram(grid):                                                            #CREATES HISTOGRAM OF GREYSCALE PIXEL COLOUR FREQUENCIES
    hist = [0] * 256                                                            #CREATE LIST FOR ALL POSSIBLE GREYSCALE VALUES (0 TO 255)                          
    for y in range(len(grid)):                                                  #LOOP THROUGH ROWS OF GRID
        for x in range(len(grid[y])):                                           #LOOP THROUGH GREYSCALE VALUES IN ROW
            hist[grid[y][x]] += 1                                            
    return hist                                                                 #RETURNS HISTOGRAM OF GREYSCALE PIXEL AMOUNTS AS AN INT LIST


def threshold_value(hist, width, height):                                       #CALCULATES T-VALUE FOR HISTOGRAM USING OTSU'S METHOD
    total_pixels = width*height                                                 #proper name
    class_variances = []                                                        #CLASS VARIANCE FOR EACH T-VALUE 
    mean_values = []                                                            #MEAN VALUES STORED TO AVOID REPEATED CALCULATION 
    for i in range(len(hist)): 
        mean_values.append(i*hist[i])                                           #MEAN VALUE = LUMINANCE * FREQUENCY
    
    for t in range(len(hist)+1):                                                #LOOP THROUGH POSSIBLE T-VALUES FROM HISTOGRAM
        weight_fg = sum(hist[t:])/total_pixels                                  #CALCULATE FOREGROUND & BACKGROUND WEIGHTS & MEANS
        weight_bg = sum(hist[:t])/total_pixels 
        if sum(hist[t:]) == 0:                                                  #AVOID DIVISION BY ZERO IF ZERO FREQUENCY
            mean_fg = 0
        else:
            mean_fg = sum(mean_values[t:])/sum(hist[t:])
        if sum(hist[:t]) == 0:
            mean_bg = 0
        else:
            mean_bg = sum(mean_values[:t])/sum(hist[:t])
        class_variances.append(weight_bg*weight_fg*(mean_bg-mean_fg)**2)        #CALCULATE CLASS VARIANCE
    return class_variances.index(max(class_variances))                          #RETURNS CORRECT T-VALUE (ONE WITH HIGHEST CLASS VARIANCE)
    

def threshold(grid):                                                            #THRESHOLDS AN RGB GRID USING OTSU'S METHOD
    hist = histogram(grid)
    t = threshold_value(hist, len(grid[0]), len(grid))                          #USE OTSU'S METHOD TO FIND APPROPRIATE THRESHOLD

    for y in range(len(grid)):                                                  #LOOP THROUGH ROWS OF GREYSCALE GRID
        for x in range(len(grid[y])):                                           #LOOP THROUGH GREYSCALE VALUES
            if grid[y][x] > t:                                                  #BINARY BASED ON WHETHER LUMINANCE IS ABOVE/BELOW T-VALUE
                grid[y][x] = 0
            else:
                grid[y][x] = 1
    return grid                                                                 #RETURNSTWO DIMENSIONAL BINARY GRID

    
def csv(grid):
    csv_string = ''
    for row in grid:
        for item in row:
            csv_string += str(item).replace(', ', ' - ').replace('[','').replace(']','') + ','
        csv_string = csv_string[:-1] + '\n'
    return csv_string[:-1]


def grid(csv):
    grid = csv.split('\n')
    for y in range(len(grid)):
        grid[y] = grid[y].split(',')
        for x in range(len(grid[y])):
            try:
                grid[y][x] = int(grid[y][x])
            except:
                del grid[y][x]
    return grid
   
            
def crop(grid):
    csv_path = '/Users/danarmstrong/Desktop/Coursework/threshold.csv' #Make them responsive
    cmd_path = '/usr/local/bin/Rscript'
    script_path = '/Users/danarmstrong/Desktop/Coursework/crop_image.r'
    csv_text = csv(grid)
    file = open(csv_path, 'w')
    file.write(csv_text)
    file.close()
    subprocess.check_output([cmd_path, script_path, csv_path], universal_newlines=True)
    
    
def display(grid):
    display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
    pixels = display_image.load()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                pixels[x,y] = (255,255,255)
            elif grid[y][x] == 1:
                pixels[x,y] = (0,0,0)
            elif type(grid[y][x]) == int:
                pixels[x,y] = (grid[y][x], grid[y][x], grid[y][x])
            else:
                pixels[x,y] = (grid[y][x][0], grid[y][x][1], grid[y][x][2])
    display_image.show()

