from PIL import Image as PIL                                                    #ALIAS DEFINED FOR SUB-MODULE AS SIMILAR NAME USED FOR CLASS
from PIL import ImageTk, ImageDraw
from tkinter import *
import threading
import subprocess
import os

import path                                                                     #CUSTOM MODULES
import update
import csv
import structures

class Invalid(Exception):                                                       #CUSTOM ERROR RAISED WHEN VALIDATION CHECKS FAIL
    pass


class Exception_Thread(threading.Thread):                                       #CUSTOM THREAD CLASS TO ACCOMODATE EXCEPTIONS
    def run(self):
        self.thread_invalid = False
        self.thread_quit = False
        self.invalid_message = ''
        try:
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
            finally:
                del self._target, self._args, self._kwargs

        except Invalid as e:                                                    #CATCHES CUSTOM ERRORS
            self.thread_invalid = True
            info = e.args
            if len(info) > 0 : self.invalid_message = info[0]
        
        except update.Quit:
            self.thread_quit = True

    def join(self):                                                             #RETURNS DETAILS ABOUT EXCEPTIONS
        threading.Thread.join(self)
        if self.thread_invalid : return 'i ' + self.invalid_message
        if self.thread_quit : return 'q'
        return ''
    

class Image():                                                                  #IMAGE CLASS - STORES/MANIPLUATES IMAGE DATA
    def __init__(self, image_file, rectilinear):
        self.image_name = image_file
        self.maze_csv_name = None
        self.wall_csv_name = None
        self.rectilinear = rectilinear
        self.edited = False
        self.inverted = False
        self.cell_size = None
        self.wall_size = None
        self.end_points = [-1,-1,-1,-1]
        self.nodes = None
        self.path = []
        self.path_colour_one = [0, 0, 255]
        self.path_colour_two = [255, 0, 0]

        update.set_update('Loading Image')                                      #CATCH FILE OPENING ERRORS
        try : self.img_data = PIL.open(self.image_name)
        except : raise Invalid('Error whilst opening the image - it may be corrupted or currently in use')
        self.width = self.img_data.size[0]
        self.height = self.img_data.size[1]

    def is_rectilinear(self):                                                   #GETTERS AND SETTERS
        return self.rectilinear
    def is_edited(self):
        return self.edited

    def get_cell_size(self):
        return self.cell_size
    def get_wall_size(self):
        return self.wall_size
    def get_maze_csv_name(self):
        return self.maze_csv_name
    def get_end_points(self):
        return self.end_points

    def set_end_points(self, value):
        if not isinstance(value, list) : raise TypeError('Value must be of type list')
        if not all(isinstance(x, int) for x in value) : raise TypeError('End points must be integers')
        if len(value) != 4 : raise ValueError('There must be 4 end point values')
        grid = csv.open_integer_grid(self.maze_csv_name)
        try : test = grid[value[1]][value[0]] + grid[value[3]][value[2]]
        except : raise ValueError('End points must be within maze boundaries')
        self.end_points = value
    def set_edited(self):
        self.edited = True
    def set_path_colours(self, one, two):
        try:
            test = int(one[0]) + int(one[1]) + int(one[2]) + int(two[0]) + int(two[1]) + int(two[2])
            if len(one) > 3 : raise ValueError
            if len(two) > 3 : raise ValueError
            for x in one + two:
                if not 0 <= x <= 255 : raise ValueError
            self.path_colour_one = one
            self.path_colour_two = two
        except : raise Invalid('Colours must be integer lists in the form [R,G,B]')
    def reset_end_points(self):
        self.end_points = [-1, -1, -1, -1]
        
    def rgb(self):                                                              #RETURNS 2D GRID OF RGB VALUES
        update.set_update('Converting To RGB')                                  
        try : return self.img_data.convert('RGB')                               #CATCH ERRORS WHILST CONVERTING
        except : raise Invalid('Error whilst converting the image - it may be corrupted')
        
    def greyscale(self):                                                        #RETURNS 2D GRID OF INTEGER GREYSCALE VALUES                                                      
        grid = []                                                               
        rgb_data = self.rgb()
        pixels = rgb_data.load()                                                #ALLOWS ACCESS TO PIXEL DATA
        for y in range(self.height):                                            
            update.set_update('Creating Greyscale ' + str(round(y/self.height*100)) + ' %')
            grid.append([])
            for x in range(self.width):
                r_luminance = pixels[x,y][0]*0.2126
                g_luminance = pixels[x,y][1]*0.7152
                b_luminance = pixels[x,y][2]*0.0722
                luminance = round(r_luminance + g_luminance + b_luminance)      
                grid[y].append(luminance)                                       
        return grid

    def generate_maze(self):                                                    #CREATES MAZE GRID USING R MODULES
        directory = os.getcwd()
        cmd_path = '/usr/local/bin/Rscript'
        script_path = directory + '/maze.r'
        greyscale_csv = 'greyscale.csv'  
        input_text = directory + ' ' + greyscale_csv + ' ' + update.get_quit_file() + ' ' + update.get_update_file()
        input_text += ' ' + str(self.rectilinear) + ' ' + str(self.inverted)
        grid = self.greyscale()                                                 #CREATE GREYSCALE GRID FOR OTSU'S METHOD
        update.set_update('Saving Greyscale')
        csv.save_grid(greyscale_csv, grid)        
        update.check_quit()
                                                                                #CALL R PROGRAM AND WAIT FOR OUTPUT
        data = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True).split(' ')
        if data[0] == 'quit':                                                   #QUIT IF R PROGRAM HAS BEEN QUIT
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

    def display_maze(self):                                                     #RETURNS PIL IMAGE OF MAZE GRID
        grid = csv.open_integer_grid(self.maze_csv_name)
        display_image = PIL.new('RGB',(len(grid[0]),len(grid)))
        pixels = display_image.load()
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:                                             #BINARY MAZE GRID REPRESENTED BY BLACK/WHITE PIXELS
                    pixels[x,y] = (255,255,255)
                elif grid[y][x] == 1:
                    pixels[x,y] = (0,0,0)
        return display_image

    def invert_maze(self):                                                      #SWITCHES INVERTETED STATE
        self.inverted = not self.inverted
        
    def generate_points(self):                                                  #AUTO-GENERATES END POINTS 
        maze = csv.open_integer_grid(self.maze_csv_name)
        self.end_points = [-1, -1, -1, -1]

        for y in [0, len(maze)-1]:                                              #SEARCH FIRST AND LAST ROW FOR PATH CELL
            if -1 not in self.end_points[2:4] : break                           #RETURN IF BOTH POINTS FOUND
            for x in range(len(maze[y])):
                update.check_quit()
                if maze[y][x] == 0 and -1 in self.end_points[0:2]:              #IF NEITHER POINT FOUND YET
                    self.end_points[0:2] = [x, y]
                elif maze[y][x] == 0:
                    self.end_points[2:4] = [x, y]
                    break

        for x in [0, len(maze[0])-1]:                                           #DO THE SAME WITH FIRST AND LAST COLUMN
            if -1 not in self.end_points[2:4] : break 
            for y in range(len(maze)):
                update.check_quit()
                if maze[y][x] == 0 and -1 in self.end_points[0:2]:
                    self.end_points[0:2] = [x, y]
                elif maze[y][x] == 0:
                    self.end_points[2:4] = [x, y]
                    break

    def display_points(self):                                                   #RETURNS PIL IMAGE OF MAZE WITH END POINTS OVERLAYED
        display_image = self.display_maze()
        pixels = display_image.load()
        pixels[self.end_points[0],self.end_points[1]] = (250,2,60)
        pixels[self.end_points[2],self.end_points[3]] = (250,2,60)
        return display_image

    def generate_nodes(self):                                                   #FINDS NODES USING R MODULES
        directory = os.getcwd()
        cmd_path = '/usr/local/bin/Rscript'
        input_text = directory + ' ' + self.maze_csv_name + ' ' + update.get_quit_file() + ' ' + update.get_update_file()
        script_path = directory + '/rectangles.r'
        if not self.rectilinear:                                                #USE RSR TO REDUCE NODE AMOUNTS FOR NON-RECTILINEAR 
            rect_csv_file = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True)
            if rect_csv_file == 'quit':
                raise update.Quit

        input_text += ' ' + str(self.rectilinear)
        script_path = directory + '/nodes.r'
        for point in self.end_points : input_text += ' ' + str(point+1)         #INCREMENT INDEXES AS R STARTS AT 1 NOT 0
        if not self.rectilinear : input_text += ' ' + rect_csv_file
                                                                                #CALL R PROGRAM AND WAIT FOR OUTPUT
        data = subprocess.check_output([cmd_path, script_path, input_text], universal_newlines=True)
        if data == 'quit':                                                      #QUIT IF R PROGRAM HAS BEEN QUIT
            raise update.Quit
        nodes_grid = csv.open_integer_grid(data)
        self.nodes = structures.Hash_Table(len(nodes_grid))                     #HASH TABLE OF NODES AND NEIGHBOURS
        for node in nodes_grid:                                                 #JOIN NODES TOGETHER IN BOTH DIRECTIONS
            node_id = str(node[0]) + '-' + str(node[1])
            self.nodes[node_id] = []
            if node[2] != -1:
                nbr_id = str(node[2]) + '-' + str(node[1])
                self.nodes[node_id].append(nbr_id)
                self.nodes[nbr_id].append(node_id)
            if node[3] != -1:
                nbr_id = str(node[0]) + '-' + str(node[3])
                self.nodes[node_id].append(nbr_id)
                self.nodes[nbr_id].append(node_id)

    def generate_path(self):                                                    #USE PYTHON MODULE TO GENERATE SHORTEST PATH
        start_pos = [self.end_points[0], self.end_points[1]]
        end_pos = [self.end_points[2], self.end_points[3]]
        self.path = path.shortest_path(self.nodes, start_pos, end_pos)

    def path_colour(self, current, total):
        r = round((self.path_colour_one[0]*current + self.path_colour_two[0]*(total-current)) / total)
        g = round((self.path_colour_one[1]*current + self.path_colour_two[1]*(total-current)) / total)
        b = round((self.path_colour_one[2]*current + self.path_colour_two[2]*(total-current)) / total)
        return (r, g, b)
    
    def display_path(self):                                                     #RETURNS PIL IMAGE OF MAZE WITH PATH OVERLAYED
        if self.path == None : return None
        total = len(self.path)

        if self.rectilinear and not self.edited:                                #ALLOWS PATH TO BE OVERLAYED ON ORIGINAL IMAGE
            display_image = self.rgb()
            walls = csv.open_integer_grid(self.wall_csv_name)
            draw = ImageDraw.Draw(display_image)                                #ALLOWS SHAPES TO BE DRAWN ON IMAGE
            prev = self.path[0]
            for i, point in zip(range(total), self.path):
                if prev[0] % 2 == 0:
                    x1 = round(walls[prev[0]//2][0] + self.wall_size / 2)       #CONVERTS PATH INDEX TO PIXEL POS USING WALL POS
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
                                                                                #USE COLOUR GRADIENT TO DRAW PATH
                draw.line((x1,y1,x2,y2), fill=self.path_colour(i, total))
                prev = point
            return display_image

        if self.edited:                                                         #IF EDITED MAZE GRID MUST BE USED
            display_image = self.display_maze()
            draw = ImageDraw.Draw(display_image)
            prev = self.path[0]
            for i, point in zip(range(total), self.path):
                draw.line((prev[0],prev[1],point[0],point[1]), fill=self.path_colour(i, total))
                prev = point
            return display_image

        else:                                                                   #IF UNEDITED PATH CAN BE OVERLAYED ON ORIGINAL
            display_image = self.rgb()
            draw = ImageDraw.Draw(display_image)
            prev = self.path[0]
            for i, point in zip(range(total), self.path):
                draw.line((prev[0],prev[1],point[0],point[1]), fill=self.path_colour(i, total))
                prev = point
            return display_image

    def save_image(self, image, path = False):                                  #SAVES PIL IMAGE AND RETURNS FILE NAME USED
        try:
            if path:
                sections = self.image_name.split('.')                           #IF SAVING PATH USE DIFFERENT FILENAME
                name = '.'.join(sections[:-1])
                name += '-path'
                name += '.' + sections[-1]
                image.save(name)
                return name
            else:
                self.img_data = image
            image.save(self.image_name)
            return self.image_name
        except:
            raise Invalid('Error whilst saving the image - please try again')
                
            
class Window(Frame):                                                            #WINDOW CLASS TO GROUP GUI TOGETHER
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
        self.maze_object = None                                                 #OBJECT TO ENCAPSULATE MAZE DATA
        self.display_image = None                                               #IMAGE DISPLAYED ON CANVAS

        self.display_frame = Frame(self)
        self.button_frame = Frame(self, bg=self.buttons_bg)
        self.display_canvas = Canvas(self.display_frame, width=self.canvas_width, height=self.canvas_height, highlightthickness=0)
        self.update_text = self.display_canvas.create_text(self.width*0.5,self.height*0.45, anchor=CENTER, text='')
                                                                                #UPDATE TEXT DISPLAYS USEFUL INFO TO USER
        self.load_button = Button(self.button_frame, text='Load Image', command=self.load_maze, highlightbackground=self.buttons_bg)
        self.draw_button = Button(self.button_frame, text='Draw Maze', command=self.draw_maze, highlightbackground=self.buttons_bg)
        self.edit_button = Button(self.button_frame, text='Edit Maze', command=self.edit_maze, highlightbackground=self.buttons_bg)
        self.invert_button = Button(self.button_frame, text='Invert Maze', command=self.invert_maze, highlightbackground=self.buttons_bg)
        self.select_button = Button(self.button_frame, text='Select Points Manually', command=self.select_points,
                                    highlightbackground=self.buttons_bg)
        self.auto_select_button = Button(self.button_frame, text='Auto-Select Points', command=self.auto_select_points,
                                         highlightbackground=self.buttons_bg)
        self.solve_button = Button(self.button_frame, text='Solve Maze', command=self.find_path, highlightbackground=self.buttons_bg)
        self.save_button = Button(self.button_frame, text='Save Maze', command=self.save_maze, highlightbackground=self.buttons_bg)
        self.colour_button = Button(self.button_frame, text='Change Path Colours', command=self.change_colours,
                                    highlightbackground=self.buttons_bg)
        self.return_button = Button(self.button_frame, text='Return to Menu', command=self.return_home, highlightbackground=self.buttons_bg)
        self.back_button = Button(self.button_frame, text='Go Back', command=self.go_back, highlightbackground=self.buttons_bg)
        self.help_button = Button(self.button_frame, text='Help', command=self.display_help, highlightbackground=self.buttons_bg)
        self.preview_button = Button(self.button_frame, text='View Larger Image', command=self.display_preview,
                                     highlightbackground=self.buttons_bg)

        self.create_window()
        self.main_menu()

    def update(self):                                                           #CALLED EVERY FRAME TO DEAL WITH THREADS
        if self.state == 'creating':
            if self.thread.is_alive():                                          #WHILST THREAD IS RUNNING DISPLAY INFO
                update_text = update.get_update()
                if update_text != '':
                    self.display_canvas.itemconfig(self.update_text, text=update_text)
            else:                                                               #DEAL WITH FINISHED THREAD
                thread_info = self.thread.join().split(' ')
                if thread_info[0] == 'i':                                       #VALIDATION ERROR
                    if len(thread_info) > 1:
                        message = ' '.join(thread_info[1:])
                        messagebox.showwarning('Error whilst opening', message)

                    self.main_menu()
                elif thread_info[0] == 'q' : self.main_menu()                   #QUIT ERROR
                else : self.display_maze()
                self.thread = None            

        elif self.state == 'drawing':                                           #MAZE IS BEING DRAWN IN PROCESSING
            if not self.thread.is_alive():
                thread_info = self.thread.join().split(' ')
                if thread_info[0] == 'q' : self.main_menu()
                else:
                    self.display_maze()
                    self.save_maze()
                self.thread = None            

        elif self.state == 'editing':                                           #MAZE IS BEING EDITED IN PROCESSING
            if not self.thread.is_alive():
                thread_info = self.thread.join().split(' ')
                if thread_info[0] == 'q' : self.main_menu()
                else : self.display_maze()
                self.thread = None            

        elif self.state == 'selecting':                                         #END POINTS BEING SELECTED IN PROCESSING
            if not self.thread.is_alive():
                thread_info = self.thread.join().split(' ')
                if thread_info[0] == 'q' : self.main_menu()
                elif -1 in self.maze_object.get_end_points():
                    messagebox.showwarning('Unselected end points', 'Two end points must be selected to continue')
                    self.display_maze()
                else:
                    self.display_points()
                self.thread = None

        elif self.state == 'finding':                                           #PATH BEING FOUND
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

    def create_window(self):                                                    #SETS UP WINDOW STRUCTURE
        self.master.title("Maze Solver")
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.pack(fill=BOTH, expand=1)

        self.button_frame.pack(fill=X)
        self.display_frame.pack()
        self.display_canvas.pack()

    def add_buttons(self, buttons):                                             #ADDS SPECIFIC BUTTONS TO BUTTON FRAME
            for button in self.button_frame.winfo_children():
                button.grid_forget()                                            #REMOVE CURRENT BUTTONS

            grid_width = self.width / len(buttons)
            self.button_frame.rowconfigure(0, minsize=self.height*0.075)
            for x in range(len(buttons)):
                buttons[x].grid(row=0,column=x)                                 #PACK BUTTONS EVENLY
                self.button_frame.columnconfigure(x, minsize=grid_width)

    def main_menu(self):                                                        #SETS UP WINDOW FOR MAIN MENU                                                       
        self.state = 'main'
        self.add_buttons([self.load_button, self.draw_button, self.help_button])
        self.display_canvas.itemconfig(self.update_text, text='Draw or load maze to start')

    def creating_menu(self):                                                    #SETS UP WINDOW WHILST MAZE BEING SCANNED 
        self.state = 'creating'
        self.add_buttons([self.return_button, self.help_button])

    def image_menu(self):                                                       #SETS UP WINDOW FOR WHEN IMAGE BEING DISPLAYED
        self.state = 'image'
        self.add_buttons([self.edit_button, self.invert_button, self.select_button, self.auto_select_button,
                          self.preview_button, self.return_button, self.help_button])
        if self.maze_object.is_rectilinear() : self.auto_select_button.config(state='active')
        else : self.auto_select_button.config(state='disabled')

    def draw_menu(self):                                                        #SETS UP WINDOW FOR WHEN MAZE IS BEING DRAWN 
        self.state = 'drawing'
        self.add_buttons([self.return_button, self.help_button])

    def edit_menu(self):                                                        #SETS UP WINDOW FOR WHEN MAZE IS BEING EDITED  
        self.state = 'editing'
        self.add_buttons([self.return_button, self.help_button])

    def selecting_menu(self):                                                   #SETS UP WINDOW FOR WHEN POINTS ARE BEING SELECTED 
        self.state = 'selecting'
        self.add_buttons([self.return_button, self.help_button])

    def points_menu(self):                                                      #SETS UP WINDOW FOR WHEN POINTS ARE BEING DISPLAYED 
        self.state = 'points'
        self.add_buttons([self.back_button, self.preview_button, self.solve_button, self.return_button, self.help_button])
    
    def finding_menu(self):                                                     #SETS UP WINDOW FOR WHEN PATH IS BEING FOUND 
        self.state = 'finding'
        self.add_buttons([self.return_button, self.help_button])

    def path_menu(self):                                                        #SETS UP WINDOW FOR WHEN PATH ARE BEING DISPLAYED 
        self.state = 'path'
        self.add_buttons([self.back_button, self.save_button, self.colour_button, self.preview_button, self.return_button, self.help_button])

    def get_file(self):                                                         #RETURNS IMAGE FILE FROM DIALOG
        self.master.update()                                                
        file_name = filedialog.askopenfilename(filetypes =(('Images', '*.png'),('Images', '*.gif'),('Images', '*.jpg')), title = 'Select Image')
        self.master.update()                                                    #UPDATE BEFORE/AFTER TO STOP TKINTER CRASHING
        return file_name

    def load_maze(self):                                                        #LOADS IMAGE VIA THREAD
        file_name = self.get_file()
        if file_name != '':
            update.set_quitting(False)                                          #RESET QUIT FILE
            if messagebox.askyesno('Maze Type', 'Is this maze rectilinear?') : rectilinear = True
            else : rectilinear = False
            self.thread = Exception_Thread(target = self.call_load, args = [file_name, rectilinear])
            self.thread.start()
            self.creating_menu()

    def draw_maze(self):                                                        #DRAWS MAZE VIA THREAD
        update.set_quitting(False)
        width = simpledialog.askinteger('Maze Dimensions', 'Enter maze width below', minvalue=2, maxvalue=500)
        if not width : return
        height = simpledialog.askinteger('Maze Dimensions', 'Enter maze height below', minvalue=2, maxvalue=500)
        if not height : return
        name = simpledialog.askstring('Maze Dimensions', 'Enter maze name below')
        if not name : return
        self.thread = Exception_Thread(target = self.call_draw, args = [width, height, name + '.png'])
        self.thread.start()
        self.display_canvas.itemconfig(self.update_text, text='Maze currently being drawn')
        self.draw_menu()

    def edit_maze(self):                                                        #EDITS MAZE VIA THREAD
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_edit)
        self.thread.start()
        self.display_canvas.delete('image')
        self.display_canvas.itemconfig(self.update_text, text='Maze currently being edited')
        self.maze_object.set_edited()
        self.edit_menu()

    def invert_maze(self):                                                      #LOADS IMAGE BUT INVERTS THRESHOLD
        self.display_canvas.delete('image')
        self.thread = Exception_Thread(target = self.call_invert)
        self.thread.start()
        self.creating_menu()

    def save_maze(self):                                                        #SAVES MAZE AS A IMAGE FILE
        try:
            if self.state == 'path':
                file_name = self.maze_object.save_image(self.display_image, True)
                messagebox.showinfo('Path saved', 'The maze route has been saved as ' + file_name)
            else:
                self.maze_object.save_image(self.display_image)
        except Invalid as e:
            message = e.args[0]
            messagebox.showwarning('Error whilst saving', message)

        
    def select_points(self):                                                    #SELECT END POINTS VIA THREAD
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_select)
        self.thread.start()
        self.display_canvas.delete('image')
        self.display_canvas.itemconfig(self.update_text, text='End points being selected')
        self.selecting_menu()

    def auto_select_points(self):                                               #FIND END POINTS AUTOMATICALLY VIA THREAD
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.maze_object.generate_points)
        self.thread.start()
        self.selecting_menu()                           

    def find_path(self):                                                        #FIND PATH VIA THREAD
        update.set_quitting(False)
        self.thread = Exception_Thread(target = self.call_find)
        self.thread.start()
        self.display_canvas.delete('image')
        self.finding_menu()

    def change_colours(self):                                                   #CHANGE THE COLOUR GRADIENT OF THE PATH
        try:
            colour_input = simpledialog.askstring('Path Colours', 'Enter starting path colour below in the form R,G,B')
            colour_one = list(map(int, colour_input.replace(' ','').split(',')))
            colour_input = simpledialog.askstring('Path Colours', 'Enter end path colour below in the form R,G,B')
            colour_two = list(map(int, colour_input.replace(' ','').split(',')))
            self.maze_object.set_path_colours(colour_one, colour_two)
            self.display_path()
        except:
            messagebox.showwarning('Invalid', 'Both colours must be in the form R,G,B where these are integers between 0 and 255')

    def display_maze(self):                                                     #DISPLAY MAZE ON CANVAS TO USER
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_object.display_maze()                    #RESIZE IMAGE TO FIT ON CANVAS
        scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
        resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
        self.display_canvas.background = ImageTk.PhotoImage(resized)
        self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2,
                                         image=self.display_canvas.background, anchor=CENTER, tags='image')
        self.image_menu()
        if scale < 1.75:                                                        #BELOW THIS MAZE GETS DISTORTED
            message = 'The maze may be too large to be accurately displayed in the quick view'
            message += '- please press "View Larger Image"'
            messagebox.showwarning('Large maze detected', message)
        
    def display_points(self):                                                   #DISPLAY MAZE WITH POINTS OVERLAYED
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_object.display_points()
        scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
        resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
        self.display_canvas.background = ImageTk.PhotoImage(resized)
        self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2,
                                         image=self.display_canvas.background, anchor=CENTER, tags='image')
        self.points_menu()
        if scale < 1.75:
            message = 'The maze may be too large to be accurately displayed in the quick view'
            message += '- please press "View Larger Image"'
            messagebox.showwarning('Large maze detected', message)

    def display_path(self):                                                     #DISPLAY MAZE WITH PATH OVERLAYED
        self.display_canvas.itemconfig(self.update_text, text='')
        self.display_image = self.maze_object.display_path()
        if self.display_image == None:                                          #NO PATH FOUND SO RETURN TO PREVIOUS MENU
            messagebox.showwarning('Path not found', 'There are no paths between the two points selected - please select different end points')
            self.maze_object.reset_end_points()
            self.display_maze()
        else:
            scale = min((self.canvas_width*0.9) / self.display_image.size[0], (self.canvas_height*0.9) / self.display_image.size[1])
            resized = self.display_image.resize((round(self.display_image.size[0]*scale), round(self.display_image.size[1]*scale)))
            self.display_canvas.background = ImageTk.PhotoImage(resized)
            self.display_canvas.create_image(self.canvas_width/2, self.canvas_height/2,
                                             image=self.display_canvas.background, anchor=CENTER, tags='image')
            self.path_menu()
            if scale < 1:
                message = 'The maze may be too large to be accurately displayed in the quick view'
                message += '- please press "View Larger Image"'
                messagebox.showwarning('Large maze detected', message)

    def display_preview(self):                                                  #OPENS IMAGE FILE USING OS SOFTWARE (I.E. PREVIEW)
        self.display_image.show()

    def display_help(self):                                                     #DISPLAY HELP DEPENDING ON STATE
        if self.state == 'main':
            message = 'Press ‘Load Image’ to load a maze from an image file.'
            message += ' ' + 'You will be asked to select the file via a file browser.'
            message += '\n\n' + 'Press \'Draw Maze\' to create a maze from scratch, using drawing software.'
            message += ' ' + 'You will be asked to specify the width and height of the image in pixels, as well as a name for the maze.'
        elif self.state == 'creating':
            message = 'The maze is currently being analysed and converted into a binary grid.'
            message += ' ' + 'If you would like to return to the main menu and stop this analysis, press \'Return Home\'.'
        elif self.state == 'drawing':
            message = 'The maze is currently being drawn using the Processing program.'
            message += ' ' + 'If you would like to return to the main menu and stop this, press \'Return Home\'.'
        elif self.state == 'editing':
            message = 'The maze is currently being edited using the Processing program.'
            message += ' ' + 'If you would like to return to the main menu and stop this, press \'Return Home\'.'
        elif self.state == 'selecting':
            message = 'The end points are currently being selected using the Processing program.'
            message += ' ' + 'If you would like to return to the main menu and stop this, press \'Return Home\'.'
        elif self.state == 'finding':
            message = 'The solution to the maze is currently being found.'
            message += ' ' + 'If you would like to return to the main menu and stop this algorithm, press \'Return Home\'.'
        elif self.state == 'image':
            message = 'Press \'Edit Maze\' to edit the maze using drawing software.'
            message += ' ' + 'It will open up a new window – follow the instructions there.'
            message += '\n\n' + 'Press \'Invert Maze\' to invert black and white pixels.'
            message += ' ' + 'This is used when the walls are of a lighter colour than the path in the original image.'
            message += '\n\n' + 'Press \'Select Points Manually\' to select the start and end of the route through the maze yourself.'
            message += '\n\n' + 'Press \'Auto-Select Points\' to get the program to choose end points for you.'
            message += '\n\n' + 'Press \'View Larger Image\' to display the image on the canvas in a larger format.'
            message += '\n\n' + 'If you would like to return to the main menu press \'Return Home\'.'
        elif self.state == 'points':
            message = 'Press \'Go Back\' to edit the maze or select different end points.'
            message += '\n\n' + 'Press \'View Larger Image\' to display the image on the canvas in a larger format.'
            message += '\n\n' + 'Press \'Solve Maze\' to solve the maze between the selected end points'
            message += '\n\n' + 'If you would like to return to the main menu press \'Return Home\'.'
            message += '\n\n' + 'Press \'View Larger Image\' to display the image on the canvas in a larger format.'
            message += '\n\n' + 'If you would like to return to the main menu press \'Return Home\'.'
        elif self.state == 'path':
            message = 'Press \'Go Back\' to edit the maze or select different end points.'
            message += '\n\n' + 'Press \'View Larger Image\' to display the image on the canvas in a larger format.'
            message += '\n\n' + 'Press \'Save Maze\' to save the solved maze in the form \'example-path.png\'.'
            message += '\n\n' + 'Press \'Change Path Colours\' to change the colour gradient used to draw the path.'
            message += '\n\n' + 'Press \'View Larger Image\' to display the image on the canvas in a larger format.'
            message += '\n\n' + 'If you would like to return to the main menu press \'Return Home\'.'
        messagebox.showinfo('Help', message)
        
    def call_load(self, file_name, rectilinear):                                #THREADED FUNCTION TO LOAD MAZE FROM IMAGE
        self.maze_object = Image(file_name, rectilinear)
        self.maze_object.generate_maze()

    def call_draw(self, width, height, file_name):                              #THREADED FUNCTION TO DRAW MAZE 
        image = PIL.new('RGB',(width, height))
        image.save(file_name, 'PNG')
        self.maze_object = Image(file_name, False)
        self.maze_object.generate_maze()

        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/build'   #CALL PROCESSING PROGRAM AND WAIT FOR OUTPUT
        output = subprocess.check_output([cmd_path, script_path, '--run', '0', update.get_quit_file(), self.maze_object.get_maze_csv_name(),
                                          str(self.maze_object.get_cell_size()), str(self.maze_object.get_wall_size())],
                                          universal_newlines=True).split('\n')
        
        if output[0] == 'quit' : raise update.Quit                              #QUIT IF PROCESSING WINDOW QUIT

    def call_edit(self):                                                        #THREADED FUNCTION TO EDIT MAZE
        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/build'
        output = subprocess.check_output([cmd_path, script_path, '--run', '1', update.get_quit_file(), self.maze_object.get_maze_csv_name(),
                                          str(self.maze_object.get_cell_size()), str(self.maze_object.get_wall_size())],
                                          universal_newlines=True).split('\n')
        if output[0] == 'quit' : raise update.Quit

    def call_invert(self):                                                      #THREADED FUNCTION TO INVERT MAZE IMAGE
        self.maze_object.invert_maze()
        self.maze_object.generate_maze()                                        #RELOADS MAZE IN ITS INVERTED FORM

    def call_select(self):                                                      #THREADED FUNCTION TO SELECT POINTS
        cmd_path = '/usr/local/bin/processing-java'
        script_path = '--sketch=/Users/danarmstrong/Desktop/Coursework/build'   #CALL PROCESSING PROGRAM AND WAIT FOR OUTPUT
        output = subprocess.check_output([cmd_path, script_path, '--run', '2', update.get_quit_file(), self.maze_object.get_maze_csv_name(),
                                          str(self.maze_object.get_cell_size()), str(self.maze_object.get_wall_size())],
                                          universal_newlines=True).split('\n')
        if output[0] == 'quit' : raise update.Quit
        self.maze_object.set_end_points(list(map(int, output[0].split(' '))))   #SET END POINTS FROM OUTPUT

    def call_find(self):                                                        #THREADED FUNCTION TO FIND THE PATH
        self.maze_object.generate_nodes()
        self.maze_object.generate_path()

    def return_home(self):                                                      #RETURN TO MAIN MENU
        if self.state in ['creating',  'drawing', 'editing', 'selecting', 'finding']:
            update.set_quitting(True)
        else:
            self.display_canvas.delete('image')
            self.main_menu()

    def go_back(self):                                                          #GO BACK TO IMAGE MENU
        self.display_maze()
    

root = Tk()                                                                     #RUN GUI 
root.resizable(width=False, height=False)
app = Window(root)
root.after(1,app.update)
root.mainloop()
