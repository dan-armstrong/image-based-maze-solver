from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS SIMILAR NAME USED FOR CLASS
from PIL import ImageTk, ImageDraw
from tkinter import *
import threading
import subprocess
import os

import image
import path
import update
import csv


class Exception_Thread(threading.Thread):
    def run(self):
        self.thread_quit = False
        try:
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            finally:
                del self._target, self._args, self._kwargs

        except update.Quit:
            self.thread_quit = True

    def join(self):
        threading.Thread.join(self)
        return self.thread_quit
    

class Image():
    def __init__(self, image_file, rectilinear):
        self.maze_csv_name = None
        self.wall_csv_name = None
        self.rectilinear = rectilinear
        self.cell_size = None
        self.wall_size = None
        self.end_points = [-1,-1,-1,-1]
        self.nodes = {}
        self.path = []

        update.set_update('Loading Image')
        self.img_data = PIL.open(image_file)
        self.width = self.img_data.size[0]
        self.height = self.img_data.size[1]

    def rgb(self):
        update.set_update('Converting To RGB')
        data = self.img_data.convert('RGB')
        return data.load()
        
    def greyscale(self):                                                        #CONVERTS RGB DATA INTO GREYSCALE GRID                                                       
        grid = []                                                               #TWO-DIMENSIONAL LIST OF LUMINANCE VALUES
        rgb_data = self.rgb()
        for y in range(self.height):                                            #LOOP THROUGH IMAGE ROWS
            update.set_update('Creating Greyscale ' + str(round(y/self.height*100)) + ' %')
            grid.append([])
            for x in range(self.width):                                         #LOOP THROUGH PIXELS IN ROW
                r_luminance = rgb_data[x,y][0]*0.2126                      #CALCULATE LUMINANCE VALUES FOR EACH COLOUR OF THE PIXEL
                g_luminance = rgb_data[x,y][1]*0.7152
                b_luminance = rgb_data[x,y][2]*0.0722
                luminance = round(r_luminance + g_luminance + b_luminance)      #ROUNDED SUM OF INDIVIDUAL LUMINANCES
                grid[y].append(luminance)                                       #LUMINANCE VALUE REPRESENTS THE CORRESPONDING PIXEL
        return grid                                                             #RETURNS GREYSCALE GRID AS A TWO-DIMENSIONAL INT LIST

    def generate_maze(self):
        directory = os.getcwd()
        cmd_path = '/usr/local/bin/Rscript'
        script_path = directory + '/maze.r'
        greyscale_csv = 'greyscale.csv'  
        input_text = directory + ' ' + greyscale_csv + ' ' + update.QUIT_FILE + ' ' + update.UPDATE_FILE + ' ' + str(self.rectilinear)

        grid = self.greyscale()
        update.set_update('Saving Greyscale')
        csv.save_grid(greyscale_csv, grid)        
        update.check_quit()

        data = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True).split(' ')
        if data[0] == 'quit':
            raise update.Quit
        if self.rectilinear:
            self.wall_csv_name = data[0]
            self.maze_csv_name = data[1]
            self.cell_size = float(data[2])
            self.wall_size = float(data[3])
        else:
            self.cell_size = 1
            self.wall_size = 0.5
            self.maze_csv_name = data[0]
        update.check_quit()

    def display_maze(self):
        grid = csv.open_integer_grid(self.maze_csv_name)
        display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
        pixels = display_image.load()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    pixels[x,y] = (255,255,255)
                elif grid[y][x] == 1:
                    pixels[x,y] = (0,0,0)
        return display_image

    def generate_points(self):
        maze = csv.open_integer_grid(self.maze_csv_name)
        self.end_points = [-1, -1, -1, -1]

        for y in [0, len(maze)-1]:
            if -1 not in self.end_points[2:4] : break 
            for x in range(len(maze[y])):
                update.check_quit()
                if maze[y][x] == 0 and -1 in self.end_points[0:2]:
                    self.end_points[0:2] = [x, y]
                elif maze[y][x] == 0:
                    self.end_points[2:4] = [x, y]
                    break

        for x in [0, len(maze[0])-1]:
            if -1 not in self.end_points[2:4] : break 
            for y in range(len(maze)):
                update.check_quit()
                if maze[y][x] == 0 and -1 in self.end_points[0:2]:
                    self.end_points[0:2] = [x, y]
                elif maze[y][x] == 0:
                    self.end_points[2:4] = [x, y]
                    break

    def display_points(self):
        display_image = self.display_maze()
        pixels = display_image.load()
        pixels[self.end_points[0],self.end_points[1]] = (250,2,60)
        pixels[self.end_points[2],self.end_points[3]] = (250,2,60)
        return display_image

    def generate_nodes(self):
        directory = os.getcwd()
        cmd_path = '/usr/local/bin/Rscript'
        input_text = directory + ' ' + self.maze_csv_name + ' ' + update.QUIT_FILE + ' ' + update.QUIT_FILE

        if self.rectilinear:
            script_path = directory + '/nodes.r'
            for point in self.end_points : input_text += ' ' + str(point+1) #r indexing
            file_name = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True)
            nodes_grid = csv.open_integer_grid(file_name)

            self.nodes = {} #do with structures
            for node in nodes_grid:
                node_id = str(node[0]) + '-' + str(node[1])
                self.nodes[node_id] = []
                
                if node[2] != 0:
                    nbr_id = str(node[2]) + '-' + str(node[1])
                    self.nodes[node_id].append(nbr_id)
                    self.nodes[nbr_id].append(node_id)
                if node[3] != 0:
                    nbr_id = str(node[0]) + '-' + str(node[3])
                    self.nodes[node_id].append(nbr_id)
                    self.nodes[nbr_id].append(node_id)

        else:
            script_path = directory + '/walls.r'
            file_name = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True)
            walls_grid = csv.open_integer_grid(file_name)

    def generate_path(self):
        start_pos = [self.end_points[0]+1, self.end_points[1]+1]
        end_pos = [self.end_points[2]+1, self.end_points[3]+1]
        if self.rectilinear:
            self.path = path.rectilinear_path(self.nodes, start_pos, end_pos)
        else:
            self.path = path.non_rectilinear_path(self.walls, start_pos, end_pos)
            display_image = self.display_maze()
            draw = ImageDraw.Draw(display_image)
            for p in range(len(self.path)):
                draw.line([self.path[p-1][0],self.path[p-1][1],self.path[p][0],self.path[p][1]], fill=100)
            display_image.show()
            
    def display_path(self):
        display_image = self.display_maze()
        pixels = display_image.load()
        walls = csv.open_grid(self.wall_csv_name)
        draw = ImageDraw.Draw(self.img_data)
        prev = self.path[0]

        for point in self.path:
            if prev[0] % 2 == 0:
                x1 = round(walls[prev[0]//2][0] + self.wall_size / 2)
            else:
                x1 = round(walls[prev[0]//2][0] + (self.wall_size + self.cell_size) / 2)
            if prev[1] % 2 == 0:
                y1 = round(walls[prev[1]//2][1] + self.wall_size / 2)
            else:
                y1 = round(walls[prev[1]//2][1] + (self.wall_size + self.cell_size) / 2) 

            if point[0] % 2 == 0:
                x2 = round(walls[point[0]//2][0] + self.wall_size / 2)
            else:
                x2 = round(walls[point[0]//2][0] + (self.wall_size + self.cell_size) / 2)
            if point[1] % 2 == 0:
                y2 = round(walls[point[1]//2][1] + self.wall_size / 2)
            else:
                y2 = round(walls[point[1]//2][1] + (self.wall_size + self.cell_size) / 2)

            draw.line([x1,y1,x2,y2], fill=100)
            prev = point

        return self.img_data
                
        
class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.width = 1200
        self.height = 700
        self.canvas_width = self.width
        self.canvas_height = self.height*0.925
        self.buttons_bg = '#FA023C'
        self.state = ''
        self.thread = None
        self.display_image = None

        self.display_frame = Frame(self)
        self.button_frame = Frame(self, bg=self.buttons_bg)
        self.display_canvas = Canvas(self.display_frame, width=self.canvas_width, height=self.canvas_height, highlightthickness=0)
        self.update_text = self.display_canvas.create_text(self.width*0.5,self.height*0.45, anchor=CENTER, text='')
        
        self.load_button = Button(self.button_frame, text='Load Image', command=self.load_maze, highlightbackground=self.buttons_bg)
        self.draw_button = Button(self.button_frame, text='Draw Maze', command=self.draw_maze, highlightbackground=self.buttons_bg)
        self.edit_button = Button(self.button_frame, text='Edit Maze', command=self.edit_maze, highlightbackground=self.buttons_bg)
        self.select_button = Button(self.button_frame, text='Select Points Manually', command=self.select_points, highlightbackground=self.buttons_bg)
        self.auto_select_button = Button(self.button_frame, text='Auto-Select Points', command=self.auto_select_points, highlightbackground=self.buttons_bg)
        self.solve_button = Button(self.button_frame, text='Solve Maze', command=self.find_path, highlightbackground=self.buttons_bg)
        self.save_button = Button(self.button_frame, text='Save Maze', command=self.save_maze, highlightbackground=self.buttons_bg)
        self.return_button = Button(self.button_frame, text='Return to Menu', command=self.return_home, highlightbackground=self.buttons_bg)
        self.back_button = Button(self.button_frame, text='Go Back', command=self.go_back, highlightbackground=self.buttons_bg)
        self.help_button = Button(self.button_frame, text='Help', command=self.display_help, highlightbackground=self.buttons_bg)
        self.preview_button = Button(self.button_frame, text='View Larger Image', command=self.display_preview, highlightbackground=self.buttons_bg)

        self.create_window()
        self.main_menu()

    def update(self):
        if self.state == 'creating':
            if self.thread.is_alive():
                update_text = update.get_update()
                if update_text != '':
                    self.display_canvas.itemconfig(self.update_text, text=update_text)
            else:
                thread_quit = self.thread.join()
                if thread_quit : self.main_menu()
                else : self.display_maze()
                self.thread = None            

        elif self.state in ['drawing', 'editing']:
            if not self.thread.is_alive():
                thread_quit = self.thread.join()
                if thread_quit : self.main_menu()
                else : self.display_maze()
                self.thread = None            

        elif self.state == 'selecting':
            if not self.thread.is_alive():
                thread_quit = self.thread.join()
                if thread_quit : self.main_menu()
                elif -1 in self.maze_image.end_points:
                    messagebox.showwarning('Unselected end points', 'Two end points must be selected to continue')
                    self.display_maze()
                else:
                    self.display_points()
                self.thread = None

        elif self.state == 'finding':
            if self.thread.is_alive():
                update_text = update.get_update()
                if update_text != '':
                    self.display_canvas.itemconfig(self.update_text, text=update_text)
            else:
                thread_quit = self.thread.join()
                if thread_quit : self.main_menu()
                else : self.display_path()
                self.thread = None            
        
        self.master.after(1,self.update)

    def create_window(self):
        self.master.title("Maze Solver")
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.pack(fill=BOTH, expand=1)

        self.button_frame.pack(fill=X)
        self.display_frame.pack()
        self.display_canvas.pack()

    def add_buttons(self, buttons):
            for button in self.button_frame.winfo_children():
                button.grid_forget()

            grid_width = self.width / len(buttons)
            self.button_frame.rowconfigure(0, minsize=self.height*0.075)
            for x in range(len(buttons)):
                buttons[x].grid(row=0,column=x)
                self.button_frame.columnconfigure(x, minsize=grid_width)

    def main_menu(self):
        self.state = 'main'
        self.add_buttons([self.load_button, self.draw_button, self.help_button])
        self.display_canvas.itemconfig(self.update_text, text='Draw or load maze to start')

    def creating_menu(self):
        self.state = 'creating'
        self.add_buttons([self.return_button, self.help_button])

    def image_menu(self):
        self.state = 'image'
        self.add_buttons([self.edit_button, self.select_button, self.auto_select_button, self.preview_button, self.return_button, self.help_button])
        if self.maze_image.rectilinear : self.auto_select_button.config(state='active')
        else : self.auto_select_button.config(state='disabled')

    def draw_menu(self):
        self.state = 'drawing'
        self.add_buttons([self.return_button, self.help_button])

    def edit_menu(self):
        self.state = 'editing'
        self.add_buttons([self.return_button, self.help_button])

    def selecting_menu(self):
        self.state = 'selecting'
        self.add_buttons([self.return_button, self.help_button])

    def points_menu(self):
        self.state = 'points'
        self.add_buttons([self.back_button, self.preview_button, self.solve_button, self.return_button, self.help_button])
    
    def finding_menu(self):
        self.state = 'finding'
        self.add_buttons([self.return_button, self.help_button])

    def path_menu(self):
        self.state = 'path'
        self.add_buttons([self.back_button, self.save_button, self.preview_button, self.return_button, self.help_button])

    def get_file(self):
        self.master.update() #stops crashes
        file_name = filedialog.askopenfilename(filetypes =(('Images', '*.png'),('Images', '*.gif'),('Images', '*.jpg')), title = 'Select Image')
        self.master.update()
        return file_name

    def load_maze(self):
        file_name = self.get_file()
        if file_name != '':
            update.set_quitting(False)
            if messagebox.askyesno('Maze Type', 'Is this maze rectilinear?') : rectilinear = True
            else : rectilinear = False
            self.thread = Exception_Thread(target = self.call_load, args = [file_name, rectilinear])
            self.thread.start()
            self.creating_menu()

    def draw_maze(self):
        update.set_quitting(False)
        width = simpledialog.askinteger('Maze Dimensions', 'Enter maze width below', minvalue=2, maxvalue=500)
        if not width : return
        height = simpledialog.askinteger('Maze Dimensions', 'Enter maze height below', minvalue=2, maxvalue=500)
        if not width : return
        name = simpledialog.askstring('Maze Dimensions', 'Enter maze filename (i.e example for example.png) below', minvalue=2, maxvalue=500)
        if not name : return
        self.thread = Exception_Thread(target = self.call_draw, args = [width, height, name])
        self.thread.start()
        self.display_canvas.itemconfig(self.update_text, text='Maze currently being drawn')
        self.draw_menu()

    def edit_maze(self):
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_edit)
        self.thread.start()
        self.display_canvas.delete('image')
        self.display_canvas.itemconfig(self.update_text, text='Maze currently being edited')
        self.edit_menu()

    def save_maze(self):
        print('save maze')

    def select_points(self):
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_select)
        self.thread.start()
        self.display_canvas.delete('image')
        self.display_canvas.itemconfig(self.update_text, text='End points being selected')
        self.selecting_menu()

    def auto_select_points(self):
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.maze_image.generate_points)
        self.thread.start()
        self.selecting_menu()                           

    def find_path(self):
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_find)
        self.thread.start()
        self.display_canvas.delete('image')
        self.finding_menu()

    def display_maze(self):
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_image.display_maze()
        scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
        resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
        self.display_canvas.background = ImageTk.PhotoImage(resized)
        self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2, image=self.display_canvas.background, anchor=CENTER, tags='image')
        self.image_menu()
        if scale < 1.75:
            messagebox.showwarning('Large maze detected', 'The maze may be too large to be accurately displayed in the quick view - please press "View Larger Image"')

    def display_points(self):
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_image.display_points()
        scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
        resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
        self.display_canvas.background = ImageTk.PhotoImage(resized)
        self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2, image=self.display_canvas.background, anchor=CENTER, tags='image')
        self.points_menu()
        if scale < 1.75:
            messagebox.showwarning('Large maze detected', 'The maze may be too large to be accurately displayed in the quick view - please press "View Larger Image"')

    def display_path(self):
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_image.display_path()
        scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
        resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
        self.display_canvas.background = ImageTk.PhotoImage(resized)
        self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2, image=self.display_canvas.background, anchor=CENTER, tags='image')
        self.path_menu()
        if scale < 1:
            messagebox.showwarning('Large image detected', 'The image may be too large to be accurately displayed in the quick view - please press "View Larger Image"')

    def display_preview(self):
        self.display_image.show()

    def display_help(self):
        print('save me')

    def call_load(self, file_name, rectilinear):
        self.maze_image = Image(file_name, rectilinear)
        self.maze_image.generate_maze()

    def call_draw(self, width, height):
        image = PIL.new('RGB',(width, height)
        image.save()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        for x in range(width):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    pixels[x,y] = (255,255,255)
                elif grid[y][x] == 1:
                    pixels[x,y] = (0,0,0)
        return display_image
        self.maze_image = Image(file_name, )
            
        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/edit'
        output = subprocess.check_output([cmd_path, script_path, '--run', '0', update.QUIT_FILE, self.maze_image.maze_csv_name,
                                          str(self.maze_image.cell_size), str(self.maze_image.wall_size)], universal_newlines=True).split('\n')
        if output[0] == 'quit' : raise update.Quit

    def call_edit(self):
        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/edit'
        output = subprocess.check_output([cmd_path, script_path, '--run', '1', update.QUIT_FILE, self.maze_image.maze_csv_name,
                                          str(self.maze_image.cell_size), str(self.maze_image.wall_size)], universal_newlines=True).split('\n')
        if output[0] == 'quit' : raise update.Quit

    def call_select(self):
        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/edit'
        output = subprocess.check_output([cmd_path, script_path, '--run', '2', update.QUIT_FILE, self.maze_image.maze_csv_name,
                                          str(self.maze_image.cell_size), str(self.maze_image.wall_size)], universal_newlines=True).split('\n')
        if output[0] == 'quit' : raise update.Quit
        self.maze_image.end_points = list(map(int, output[0].split(' ')))

    def call_find(self):
        self.maze_image.generate_nodes()
        self.maze_image.generate_path()

    def return_home(self):
        if self.state in ['creating',  'editing', 'selecting', 'finding']:
            update.set_quitting(True)
        else:
            self.display_canvas.delete('image')
            self.main_menu()

    def go_back(self):
        self.display_maze()
    

root = Tk()
root.resizable(width=False, height=False)
app = Window(root)
root.after(1,app.update)
root.mainloop()
