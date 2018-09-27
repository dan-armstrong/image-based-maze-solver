import convert_image
import find_path
import display_path

IMAGE_PATH = '/Users/danarmstrong/Desktop/Coursework/Mazes/7.gif'
SCRIPT_PATH = '/Users/danarmstrong/Desktop/Coursework/find_nodes.r'
IMAGE_CSV_PATH = '/Users/danarmstrong/Desktop/Coursework/image_data.csv'
MAZE_CSV_PATH = '/Users/danarmstrong/Desktop/Coursework/maze_data.csv'

threshold = convert_image.createThreshold(IMAGE_PATH)
g = threshold.split('\n')
for i in range(len(g)):
    g[i] = g[i].split(',')
    for o in range(len(g[i])):
        try:
            g[i][o] = int(g[i][o])
        except:
            pass
display_path.displayGrid(g)

nodes = convert_image.findNodes(threshold, SCRIPT_PATH, IMAGE_CSV_PATH)

grid = display_path.readCSV(MAZE_CSV_PATH)
display_path.displayGrid(grid)
path = find_path.findPath(nodes)
grid = display_path.drawPath(grid, path)

display_path.displayGrid(grid)
