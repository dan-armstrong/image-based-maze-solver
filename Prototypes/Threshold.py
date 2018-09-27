from PIL import Image
import math

img = Image.open('apple.jpeg')
rgb = img.convert('RGB').load()
greyscale_grid = []
for y in range(img.size[1]):
    greyscale_grid.append([])
    for x in range(img.size[0]):
        r_luminance = rgb[x,y][0]*0.2126
        g_luminance = rgb[x,y][1]*0.7152
        b_luminance = rgb[x,y][2]*0.0722
        luminance = round(r_luminance + g_luminance + b_luminance)
        greyscale_grid[y].append(luminance)

histogram = [0] * 256
for row in greyscale_grid:
    for luminance in row:
        histogram[luminance] += 1

threshold = 0
min_class_variance = math.inf
weighted_histogram = [0] * 256
for i in range(len(histogram)):
    weighted_histogram[i] = i*histogram[i]

for t in range(len(histogram)-1):
    weight_bg = sum(histogram[:t+1]) / sum(histogram)
    weight_fg = sum(histogram[t+1:]) / sum(histogram)
    mean_bg = sum(weighted_histogram[:t+1]) / sum(histogram[:t+1])
    mean_fg = sum(weighted_histogram[t+1:]) / sum(histogram[t+1:])
    class_variance = weight_bg * weight_fg * (weight_bg - weight_fg)**2
    if class_variance < min_class_variance:
        threshold = t
        min_class_variance = class_variance

binary_grid = []
for y in range(len(greyscale_grid)):
    binary_grid.append([])
    for x in range(len(greyscale_grid[y])):
        if greyscale_grid[y][x] > threshold:
            binary_grid[y].append(0)
        else:
            binary_grid[y].append(1)

display_image = Image.new('RGB',(len(binary_grid[0]),len(binary_grid)))
pixels = display_image.load()
for y in range(len(binary_grid)):
    for x in range(len(binary_grid[y])):
        if binary_grid[y][x] == 1:
            pixels[x,y] = (0,0,0)
        else:
            pixels[x,y] = (255,255,255)
display_image.show()

    
