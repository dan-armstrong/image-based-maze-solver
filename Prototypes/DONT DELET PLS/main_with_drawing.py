import image
import path

from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS SIMILAR NAME USED FOR CLASS
from tkinter import *
from threading import Thread
import subprocess
import math

class Image():
    def __init__(self, file_name):
        self.update('Loading image')
        self.img_data = PIL.open(file_name)
        self.rbg_data = self.rgb()
        self.width = self.img_data.size[0]
        self.height = self.img_data.size[1]
        self.maze_file = None
        self.maze_csv = None
        self.maze_dimensions = None

    def rgb(self):
        data = self.img_data.convert('RGB')
        return data.load()
        
    def greyscale(self):                                                        #CONVERTS RGB DATA INTO GREYSCALE GRID                                                       
        grid = []                                                              #TWO-DIMENSIONAL LIST OF LUMINANCE VALUES
        for y in range(self.height):                                              #LOOP THROUGH IMAGE ROWS 
            grid.append([])
            for x in range(self.width):                                       #LOOP THROUGH PIXELS IN ROW
                r_luminance = self.rbg_data[x,y][0]*0.2126                              #CALCULATE LUMINANCE VALUES FOR EACH COLOUR OF THE PIXEL
                g_luminance = self.rbg_data[x,y][1]*0.7152
                b_luminance = self.rbg_data[x,y][2]*0.0722
                luminance = round(r_luminance + g_luminance + b_luminance)          #ROUNDED SUM OF INDIVIDUAL LUMINANCES
                grid[y].append(luminance)                                      #LUMINANCE VALUE REPRESENTS THE CORRESPONDING PIXEL
        return grid                                                            #RETURNS GREYSCALE GRID AS A TWO-DIMENSIONAL INT LIST

    def maze_data(self):
        greyscale_csv = '/Users/danarmstrong/Desktop/Coursework/greyscale.csv' #Make them responsive
        cmd_path = '/usr/local/bin/Rscript'
        script_path = '/Users/danarmstrong/Desktop/Coursework/maze.r'

        self.update('Converting to greyscale')
        grid = self.greyscale()
        self.update('Saving greyscale')
        save_csv(grid, greyscale_csv)        
        data = subprocess.check_output([cmd_path, script_path, greyscale_csv], universal_newlines=True).split(' ')
        self.maze_file = data[0]
        self.maze_dimensions = data[1:]
        self.maze_csv = open_csv(self.maze_file)

    def node_data(self, maze_csv):
        cmd_path = '/usr/local/bin/Rscript'
        script_path = '/Users/danarmstrong/Desktop/Coursework/nodes.r'

        file_name = subprocess.check_output([cmd_path, script_path, maze_csv], universal_newlines=True)
        nodes_grid = open_csv(file_name)
        file = open(file_name, 'r')
        nodes_csv = file.read()
        file.close()
        csv_rows = nodes_csv.split('\n')
        nodes_grid = []
        for csv_row in csv_rows:
            grid_row = []
            csv_row = csv_row.split(',')
            for item in csv_row:
                try : grid_row.append(int(item))
                except : pass
            if len(grid_row) > 0 : nodes_grid.append(grid_row)

        adj_dict = {}
        for node in nodes_grid:
            node_id = str(node[0]) + '-' + str(node[1])
            adj_dict[node_id] = []
            
            if node[2] != 0:
                nbr_id = str(node[2]) + '-' + str(node[1])
                adj_dict[node_id].append(nbr_id)
                adj_dict[nbr_id].append(node_id)
            if node[3] != 0:
                nbr_id = str(node[0]) + '-' + str(node[3])
                adj_dict[node_id].append(nbr_id)
                adj_dict[nbr_id].append(node_id)
        return adj_dict    

    def path_data(self, adj_dict):
        start = path.get_start(adj_dict)
        end = path.get_end(adj_dict)
        return path.shortest_path(adj_dict, start, end)

    def update(self, text):
        file = open('update.txt', 'w')
        file.write(text)
        file.close()
        
    def display_path(self):
        maze_file = self.maze_data()
        adj_dict = self.node_data(maze_file)
        path = self.path_data(adj_dict)
        
        file = open(maze_file, 'r')
        maze_csv = file.read()
        file.close()
        csv_rows = maze_csv.split('\n')
        maze_grid = []
        for csv_row in csv_rows:
            grid_row = []
            csv_row = csv_row.split(',')
            for item in csv_row:
                try : grid_row.append(int(item))
                except : pass
            if len(grid_row) > 0 : maze_grid.append(grid_row)

        display_image = PIL.new('RGB',(len(maze_grid[0]),len(maze_grid)))
        pixels = display_image.load()
        for y in range(len(maze_grid)):
            for x in range(len(maze_grid[y])):
                if maze_grid[y][x] == 0:
                    pixels[x,y] = (255,255,255)
                elif maze_grid[y][x] == 1:
                    pixels[x,y] = (0,0,0)
        for p in path:
            pixels[p[0],p[1]] = (255,0,255)

        display_image.show()
        
        
class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.width = 1200
        self.height = 700
        self.canvas_width = self.width
        self.canvas_height = self.height*0.893

        self.buttons_bg = '#73626e'
        self.update_bg = '#e84a5f'
        self.canvas_bg = '#f8f4f3'
        self.wall_bg = '#2a363b'
        self.path_bg = '#1d1d29'
                
        self.maze_image = None
        self.display_center_x = self.canvas_width/2
        self.display_center_y = self.canvas_height/2
        self.display_zoom = 1
        self.state = ''
        self.creation_thread = None
        
        self.display_frame = Frame(self)
        self.button_frame = Frame(self, bg=self.buttons_bg)
        self.update_frame = Frame(self, bg=self.update_bg)
        self.display_canvas = Canvas(self.display_frame, width=self.canvas_width, height=self.canvas_height, highlightthickness=0, bg=self.canvas_bg)
        self.update_label = Label(self.update_frame, text='', bg=self.update_bg, fg=self.canvas_bg)
        
        self.load_button = Button(self.button_frame, text='Load Image', command=self.load_maze, highlightbackground=self.buttons_bg)
        self.draw_button = Button(self.button_frame, text='Draw Maze', command=self.draw_maze, highlightbackground=self.buttons_bg)
        self.edit_button = Button(self.button_frame, text='Edit Maze', command=self.edit_maze, highlightbackground=self.buttons_bg)
        self.solve_button = Button(self.button_frame, text='Solve Maze', command=self.solve_maze, highlightbackground=self.buttons_bg)
        self.save_button = Button(self.button_frame, text='Save Maze', command=self.save_maze, highlightbackground=self.buttons_bg)
        self.return_button = Button(self.button_frame, text='Main Menu', command=self.return_home, highlightbackground=self.buttons_bg)
        self.help_button = Button(self.button_frame, text='Help', command=self.display_help, highlightbackground=self.buttons_bg)

        self.create_window()
        self.main_menu()

    def create_window(self):
        self.master.title("Maze Solver")
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.pack(fill=BOTH, expand=1)

        self.button_frame.pack(fill=X)
        self.update_frame.pack(fill=X)
        self.display_frame.pack()
        self.display_canvas.pack()
        self.update_label.pack(anchor='center')

    def update(self):
        if self.state == 'creating':
            if self.creation_thread.is_alive():
                update_text = open('update.txt').read().replace('\n','')
                if update_text != '':
                    self.update_label.config(text=update_text)
            else:
                self.reset_display()
                self.display_maze()
                self.image_menu()
                self.creation_thread = None            
        self.master.after(1,self.update)

    def key_pressed(self, event):
        key = event.char.lower()
        if self.state == 'image' and key in ['w','a','s','d','z','x']:
            if key == 'w':
                self.display_center_y += 25
            if key == 'a':
                self.display_center_x += 25
            if key == 's':
                self.display_center_y -= 25
            if key == 'd':
                self.display_center_x -= 25
            if key == 'z':
                self.display_zoom *= 1.2
            if key == 'x':
                self.display_zoom = max(self.display_zoom/1.2, 1)
            self.display_canvas.delete('maze')
            self.display_maze()        

    def mouse_moved(self, event):
        if self.state == 'image':
            self.display_canvas.itemconfigure(self.display_canvas.find_closest(
                event.x, event.y), fill='blue')
            
    def add_buttons(self, buttons):
            for button in self.button_frame.winfo_children():
                button.grid_forget()

            grid_width = self.width / len(buttons)
            self.button_frame.rowconfigure(0, minsize=self.height*0.075)
            for x in range(len(buttons)):
                buttons[x].grid(row=0,column=x)
                self.button_frame.columnconfigure(x, minsize=grid_width)

    def spacer(self, master, w, h, colour=None):
        return Frame(master, width=w, height=h, bg=colour)

    def main_menu(self):
        self.state = 'main'
        self.add_buttons([self.load_button, self.draw_button, self.help_button])
        self.update_label.config(text='Draw or load maze to start')

    def creating_menu(self):
        self.state = 'creating'
        self.add_buttons([self.return_button, self.help_button])

    def image_menu(self):
        self.state = 'image'
        self.add_buttons([self.edit_button, self.solve_button, self.return_button, self.help_button])

    def finding_menu(self):
        self.state = 'finding'
        self.add_buttons([self.return_button, self.help_button])

    def path_menu(self):
        self.state = 'path'
        self.add_buttons([self.solve_button, self.save_button, self.return_button, self.help_button])

    def get_file(self):
        self.master.update()
        file_name = filedialog.askopenfilename(filetypes =(('Images', '*.png'),('Images', '*.gif'),('Images', '*.jpg')), title = 'Select Image')
        self.master.update()
        return file_name

    def load_maze(self):
        file_name = self.get_file()
        if file_name != '':
            self.creating_menu()
            self.maze_image = Image(file_name)
            self.creation_thread = Thread(target=self.maze_image.maze_data)
            self.creation_thread.daemon = True
            self.creation_thread.start()

    def draw_maze(self):
        print('draw maze')

    def edit_maze(self):
        print('edit maze')

    def solve_maze(self):
        self.solving_thread = Thread(target=self.maze_image.maze_data)
        self.solving_thread.daemon = True
        self.solving_thread.start()

    def save_maze(self):
        print('save maze')

    def return_home(self):
        self.display_canvas.delete('maze')
        self.main_menu()

    def display_help(self):
        print('save me')

    def display_maze(self):
        maze = self.maze_image.maze_csv
        maze_width = len(maze[0])
        maze_height = len(maze)
        cell_size = min(self.canvas_width/maze_width, self.canvas_height/maze_height)*self.display_zoom

        if maze_width*cell_size < self.canvas_width:
            self.display_center_x = self.canvas_width / 2
        elif maze_width*cell_size/2 < self.display_center_x:
            self.display_center_x = maze_width*cell_size/2
        elif maze_width*cell_size/2 < self.canvas_width - self.display_center_x:
            self.display_center_x = self.canvas_width - maze_width*cell_size/2
        if maze_height*cell_size < self.canvas_height:
            self.display_center_y = self.canvas_height / 2
        elif maze_height*cell_size/2 < self.display_center_y:
            self.display_center_y = maze_height*cell_size/2
        elif maze_height*cell_size/2 < self.canvas_height - self.display_center_y:
            self.display_center_y = self.canvas_height - maze_height*cell_size/2

        handle_x = self.display_center_x - maze_width*cell_size/2
        handle_y = self.display_center_y - maze_height*cell_size/2
        x_min = math.floor(max(0, maze_width/2 - self.display_center_x/cell_size))
        x_max = math.ceil(min(len(maze[0]), maze_width/2 + (self.canvas_width -self.display_center_x)/cell_size))
        y_min = math.floor(max(0, maze_height/2 - self.display_center_y/cell_size))
        y_max = math.ceil(min(len(maze), maze_height/2 + (self.canvas_height -self.display_center_y)/cell_size))

        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                if maze[y][x]:
                    x1 = (handle_x + x * cell_size)
                    x2 = (x1 + cell_size)
                    y1 = (handle_y + y * cell_size)
                    y2 = (y1 + cell_size)
                    self.display_canvas.create_rectangle(x1,y1,x2,y2,fill=self.wall_bg,width=0,tags='maze')
        self.update_label.config(text='Solve or edit maze')

    def reset_display(self):
        self.display_center_x = self.canvas_width/2
        self.display_center_y = self.canvas_height/2
        self.display_zoom = 1


def open_csv(file_name):
    file = open(file_name, 'r')
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


def save_csv(grid, file_name):
    csv_string = ''
    for row in grid:
        csv_string += str(row)[1:-1].replace(' ','') + '\n'
    file = open(file_name, 'w')
    file.write(csv_string[:-1])
    file.close()
    

root = Tk()
root.resizable(width=False, height=False)
app = Window(root)
root.after(1,app.update)
root.bind("<Key>", app.key_pressed)
root.bind("<Motion>", app.mouse_moved)
root.mainloop()



