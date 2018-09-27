import structures
import update
import csv


class Rectangle_Grid:
    def __init__(self, maze, length):
        self.maze = maze
        self.unexplored = structures.Heap(lambda x: -x.area())
        self.explored = []
        self.grid = self.create_grid()
        self.csv_name = 'rect.csv'
        self.min_length = length
        
    def create_grid(self):
        grid = []
        for row in range(len(self.maze)):
            update.set_update('Calculating Rectangles ' + str(round(row/len(self.maze)*100)) + ' %')
            grid.append([])
            for col in range(len(self.maze[0])):
                dims = self.max_rect(col, row)
                rect = Rectangle([col, row], dims)
                grid[row].append(rect)
                if self.maze[row][col] == 1:
                    rect.wall = True
                if rect.area() > 0:
                    self.unexplored.push(rect)
        return grid

    def max_rect(self, x, y, recalc = False):
        width = 1
        height = self.height_above(x, y, recalc)
        max_width = 0
        max_height = 0
        while x-(width-1) >= 0 and height >= 3:
            if self.maze[y][x-(width-1)] == 1 : break
            if recalc:
                if self.grid[y][x-(width-1)].removed : break
            if width*height > max_width*max_height and width >= 3:
                max_width = width
                max_height = height
            new_height = self.height_above(x-width, y, recalc)
            if new_height < height:
                height = new_height
            width += 1
        return [max_width, max_height]

    def height_above(self, x, y, recalc):
        if self.maze[y][x] == 1 : return 0
        prev_wall = -1
        for i in range(y-1,-1,-1):
            if self.maze[i][x] == 1:
                prev_wall = i
                break
            if recalc:
                if self.grid[i][x].removed:
                    prev_wall = i
                    break
        return y - prev_wall

    def remove_inside_rectangle(self, x, y):
        for px in self.grid[y][x].range_x():
            update.check_quit()
            for py in self.grid[y][x].range_y():
                if [px, py] != [x, y]:
                    self.grid[py][px].removed = True       

    def explore_outside_rectangle(self, x, y):
        for py in self.grid[y][x].range_y():
            px = x + 1
            while px < len(self.grid[y]):
                if self.grid[py][px].wall or self.grid[py][px].removed : break
                overflow_x = x - self.grid[py][px].min_x() + 1
                if overflow_x > 0:
                    dims = self.max_rect(px, py, True)
                    self.grid[py][px].width = dims[0]
                    self.grid[py][px].height = dims[1]
                    self.unexplored.update(self.grid[py][px].queue_index)
                px += 1

        for px in self.grid[y][x].range_x():
            py = y + 1
            while py < len(self.grid):
                if self.grid[py][px].wall or self.grid[py][px].removed : break
                overflow_y = y - self.grid[py][px].min_y() + 1
                if overflow_y > 0:
                    dims = self.max_rect(px, py, True)
                    self.grid[py][px].width = dims[0]
                    self.grid[py][px].height = dims[1]
                    self.unexplored.update(self.grid[py][px].queue_index)
                py += 1

        max_x = len(self.grid[0])
        max_y = len(self.grid)
        py = y + 1
        while py < max_y and max_x > x + 1:
            px = x + 1
            while px < max_x:
                if self.grid[py][px] == 1:
                    max_x = px
                    break
                overflow_x = x - self.grid[py][px].min_x() + 1
                overflow_y = y - self.grid[py][px].min_y() + 1
                if overflow_x > 0 and overflow_y > 0:
                    dims = self.max_rect(px, py, True)
                    self.grid[py][px].width = dims[0]
                    self.grid[py][px].height = dims[1]
                px += 1
            py += 1

    def save_rectangles(self):
        rect_count = 0
        total_rects = self.unexplored.length()
        while self.unexplored.length() > 0:
            update.set_update('Saving Rectangles ' + str(round(rect_count/total_rects*100)) + ' %')
            rect = self.unexplored.pop()
            if not rect.removed and rect.width > 0 and rect.height > 0:
                self.remove_inside_rectangle(rect.x, rect.y)
                self.explore_outside_rectangle(rect.x, rect.y)
                self.explored.append(rect)
            rect_count += 1

        rect_data = []
        for rect in self.explored:
            rect_data.append([rect.min_x()+1, rect.min_y()+1, rect.x+1, rect.y+1, rect.width, rect.height])
        csv.save_grid(self.csv_name, rect_data)

    def disp(self):
        for row in self.grid:
            out = []
            for rect in row:
                if rect.wall : out.append(['WW'])
                elif rect.removed : out.append(['RR'])
                else : out.append([rect.width,rect.height])
            print(out)
    
class Rectangle:
    def __init__(self, pos, dims, is_wall=False):
        self.x = pos[0]
        self.y = pos[1]
        self.width = dims[0]
        self.height = dims[1]
        self.wall = is_wall
        self.removed = False
        self.queue_index = None

    def area(self):
        return self.width * self.height

    def min_x(self):
        return self.x - (self.width-1)

    def min_y(self):
        return self.y - (self.height-1)

    def range_x(self):
        return range(self.min_x(), self.x+1)

    def range_y(self):
        return range(self.min_y(), self.y+1)

#a = Rectangle_Grid(csv.open_integer_grid('maze.csv'))
#a.disp()
#a.save_rectangles()
#print(csv.open_integer_grid('rect.csv'))
