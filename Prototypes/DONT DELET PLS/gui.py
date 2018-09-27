from tkinter import *


class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.width = 800
        self.height = 500
        self.create_window()

    def create_window(self):
        self.master.title("Maze Solver")
        self.master.geometry(str(self.width) + 'x' + str(self.height))
        self.pack(fill=BOTH, expand=1)

        self.option_frame = Frame(self)
        self.display_frame = Frame(self, width=self.width, height=self.height*0.9, bg='red')
        self.option_frame.pack()
        self.display_frame.pack()

        self.solve_button = Button(self.option_frame, text="Solve Maze", command=self.solve_maze)
        self.open_button = Button(self.option_frame, text="Open Maze", command=self.open_maze)
        self.save_button = Button(self.option_frame, text="Save Maze", command=self.save_maze)
        self.draw_button = Button(self.option_frame, text="Draw Maze", command=self.draw_maze)

        self.solve_button.grid(row=0,column=0)
        self.spacer(self.option_frame, self.width*0.05, self.height*0.1).grid(row=0,column=1)
        self.open_button.grid(row=0,column=2)
        self.spacer(self.option_frame, self.width*0.05, self.height*0.1).grid(row=0,column=3)
        self.save_button.grid(row=0,column=4)
        self.spacer(self.option_frame, self.width*0.05, self.height*0.1).grid(row=0,column=5)
        self.draw_button.grid(row=0,column=6)

    def get_file(self):
        self.master.update()
        file = filedialog.askopenfile(parent=self.master,mode='rb',title='Choose a file')
        self.master.update()
        return file

    def spacer(self, master, w, h):
        return Frame(master, width=w, height=h)

    def solve_maze(self):
        print('solve maze')

    def open_maze(self):
        print(self.get_file())

    def draw_maze(self):
        print('draw maze')

    def save_maze(self):
        print('save maze')

root = Tk()
root.resizable(width=False, height=False)
app = Window(root)
root.mainloop()
