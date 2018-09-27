from PIL import Image

img = Image.open('apple.jpeg')                                                  #LOAD IMAGE AS RGB PIXELS 
rgb = img.convert('RGB').load()
greyscale_grid = []
for y in range(img.size[1]):                                                    #LOOP THROUGH PIXELS AND CALCULATE LUMINANCE
    greyscale_grid.append([])
    for x in range(img.size[0]):
        r_luminance = rgb[x,y][0]*0.2126
        g_luminance = rgb[x,y][1]*0.7152
        b_luminance = rgb[x,y][2]*0.0722
        luminance = round(r_luminance + g_luminance + b_luminance)              #GREYSCALE VALUE MUST BE AN INTEGER
        greyscale_grid[y].append(luminance)

display_image = Image.new('RGB',(len(greyscale_grid[0]),len(greyscale_grid)))   #CREATE EMPTY IMAGE
pixels = display_image.load()
for y in range(len(greyscale_grid)):                                            #LOOP THROUGH PIXELS AND SET COLOURS
    for x in range(len(greyscale_grid[y])):
        luminance = greyscale_grid[y][x]
        pixels[x,y] = (luminance,luminance,luminance)                         
display_image.show()                                                            #DISPLAY GREYSCALE IMAGE


histogram = [0]*256                                                             #CREATE EMPTY HISTOGRAM
for y in range(len(greyscale_grid)):                                            #LOOP THROUGH PIXELS TO GET FREQUENCY OF LUMINANCE VALUES
    for x in range(len(greyscale_grid[y])):
        luminance = greyscale_grid[y][x]
        histogram[luminance] += 1

weighted_histogram = []                                                         #CREATE WEIGHTED HISTOGRAM
for i in range(len(histogram)):
    weighted_histogram.append(histogram[i] * i)

threshold = 0
max_class_variance = 0
for t in range(1,255):                                                          #CALCULATE CLASS VARIANCE FOR POSSIBLE ALL THRESHOLDS
    weight_fg = sum(histogram[t+1:])/sum(histogram)
    weight_bg = sum(histogram[:t+1])/sum(histogram)
    if sum(histogram[t+1:]) == 0 : mean_fg = 0                                  #AVOID DIVISION BY 0                             
    else : mean_fg = sum(weighted_histogram[t+1:]) / sum(histogram[t+1:])
    if sum(histogram[:t+1]) == 0 : mean_bg = 0                            
    else : mean_bg = sum(weighted_histogram[:t+1]) / sum(histogram[:t+1])

    class_variance = weight_fg * weight_bg * (mean_bg - mean_fg)**2
    if class_variance > max_class_variance:                                     #FIND THRESHOLD VALUE WITH MAXIMUM CLASS VARIANCE
        threshold = t
        max_class_variance = class_variance
        

threshold_grid = []                                                             #CREATE THRESHOLD GRID
for y in range(len(greyscale_grid)):                                            #COMPARE EACH PIXEL'S LUMINANCE TO THRESHOLD VALUE
    threshold_grid.append([])
    for x in range(len(greyscale_grid[y])):
        if greyscale_grid[y][x] > threshold:
            threshold_grid[y].append(0)
        else:
            threshold_grid[y].append(1)

display_image = Image.new('RGB',(len(greyscale_grid[0]),len(greyscale_grid)))   #CREATE EMPTY IMAGE
pixels = display_image.load()
for y in range(len(threshold_grid)):                                            #LOOP THROUGH PIXELS AND SET COLOUR 
    for x in range(len(threshold_grid[y])):
        if threshold_grid[y][x] == 0:
            pixels[x,y] = (255,255,255)
        else:
            pixels[x,y] = (0,0,0)
display_image.show()                                                            #DISPLAY GREYSCALE IMAGE
