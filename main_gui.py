import tkinter as tk
from tkinter import colorchooser

update_config_attr = lambda **kwargs: None
devices = []

class Photo:
    def __init__(self, root, name):
        self.image = tk.PhotoImage(file=name)
        self.label =  tk.Label(root, image=self.image)
        self.root = root
        self.resize(250,250)

    def resize(self, x, y):
        self.size_x = x
        self.size_y = y

    def place(self, x_new, y_new):
        self.label.place(x=x_new - self.size_x/2, y=y_new-self.size_y/2, width = self.size_x, height= self.size_y)    

class Button:
    def __init__(self, root, name, bg_color='gray'):
        self.but = tk.Button(root, text=name, background=bg_color)
        self.root = root
        self.height=50
        self.width=50
    
    def image(self, path):
        self.image = tk.PhotoImage(file=path)
        self.but.config(image=self.image)

    def place(self,x_new:int,y_new:int):
        self.but.place(x = x_new - self.width/2, y = y_new - self.height/2, height = self.height, width = self.width)

    def size(self, x_size, y_size):
        self.height=y_size
        self.width = x_size
    
    def complete(self):
        self.but.pack()

    def command(self, command):
        self.but.config(command=command)

    
class Color:            
    def __init__(self, color):
        self.color = color
    def change_color(self, update_config_attr):
        color_info = colorchooser.askcolor()     
        if color_info[1]:  
            self.color = color_info[1]
            print('change color callback')
            update_config_attr(background = self.color)
    def Color(self):
        return self.color

class Table:
    def __init__(self, root, rows, columns, duty):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.duty = duty
        self.table_info = []
        self.lst = []
        self.category = []
        print(f"r:{self.rows} c:{self.columns}")
        self.create_table(root)
        
        # Call create() after the window is fully initialized
        
    def update_color(self, color):
        self.color = color

    def on_entry_click(self, event, row, col):
        print(f"Entry clicked at row {row}, col {col}")
        
    def update_category(category_list):
        if(len(category_list) < len(self.category)):
            print(f"Error! category size < number of collums!")
            return
        for i in range(self.category):
            self.categore[i].config(text=string(category_list[i]))
    
    def create(self):
        # Get the width and height of the root window
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        # Calculate offsets (starting position for the table)
        offset_x = root_width * (1 - self.duty) / 2  # Center the table
        offset_y = root_height * (1 - self.duty) / 2  # Center the table
        
        # Calculate cell dimensions
        cell_width = int(root_width * self.duty / self.columns)
        cell_height = int(root_height * self.duty / self.rows)
        
        # Place each entry widget
        for j in range(self.columns):
            self.category[j].config(background = self.color)
            x = offset_x + j * cell_width
            self.category[j].place(x=x + 5, y = offset_y - 20)
            for i in range(self.rows):
                if i < len(self.lst) and j < len(self.lst[i]):
                    y = offset_y + i * cell_height
                    self.lst[i][j].config(readonlybackground = self.color, state="readonly")
                    self.lst[i][j].bind("<ButtonRelease-1>", lambda e, r=i, c=j: self.on_entry_click(e, r, c))
                    self.lst[i][j].place(x=x, y=y, width=cell_width, height=cell_height)
                    


    def create_table(self, root):
        self.lst = [[0 for x in range(self.columns)] for y in range(self.rows)] 
        self.category = [0 for x in range(self.columns)]
        for j in range(self.columns):
            self.category[j] = tk.Label(root, text = f"PlaceHolder{j}")
            for i in range(self.rows):
                self.e = tk.Entry(root, width=40, fg='blue',
                               font=('Arial', 16, 'bold'))
                self.lst[i][j] = self.e
                
                if self.table_info and i < len(self.table_info) and j < len(self.table_info[i]):
                    self.e.insert(tk.END, str(self.table_info[i][j]))
                else:
                    self.e.insert(tk.END, "")

def print_table(root, rows, collums, duty = 0.8):
    table = Table(root, rows, collums, duty)
    return table


def play_windows(root, color, r, c):
    table = print_table(root, rows= r, collums= c)
    table.update_color(color)
    color_c = Color(root['bg'])
    
    back_button = Button(root, "Main menu", color_c.Color())
    back_button.size(x_size = 100, y_size=50)
    back_button.command(lambda: (destroy(root), start_window(root, color_c)))
    back_button.place(root.winfo_width() - 50, root.winfo_height()-25)
    table.create()
    return table, back_button

def destroy(root):
    for widget in root.winfo_children():
        widget.destroy()  
# Function to open the new window
def open_new_window(root):
    # Create a Toplevel window (the new window)
    destroy(root)
    table = play_windows(root, root["bg"], 6, 10)
    
    return table

def start_window(root, color):
    
    root.config(background=color.Color())
    start_but = Button(root, "start", "pink")
    start_but.command(lambda: open_new_window(root))
    image = Photo(root, 'assets/logo.png')
    
    screen_width_w = root.winfo_screenwidth()
    screen_height_w = root.winfo_screenheight()
    screen_width_config=int(screen_width_w/2)
    screen_height_config=int(screen_height_w/2)
    start_but.size(400,150)

    image.place(screen_width_config/2, screen_height_config/2-100)    
    start_but.place(screen_width_config/2, screen_height_config/2+100)

    pallete_but=Button(root, "", color.Color())
    pallete_but.image("assets/pallete.png")
    pallete_but.size(40,40)
    pallete_but.place(screen_width_config-20, 20)

    devices = [root, pallete_but.but]
    update_config_attr = lambda **kwargs: [dev.config(**kwargs) for dev in devices]
    pallete_but.command(lambda: color.change_color(update_config_attr))
    root.geometry(f"{screen_width_config}x{screen_height_config}")
    root.update_idletasks()
    return [start_but, pallete_but, image]


def main():
    global devices, update_config
    root = tk.Tk()
    color = Color('#6F6FF0')
    devices = start_window(root, color)
    
    root.mainloop()
    # change_color(update_config_attr)
    
    
    return



if __name__ =="__main__":
    
    main()
