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

    def place(self,x_new,y_new):
        self.but.place(x = x_new - self.width/2, y = y_new - self.height/2, height = self.height, width = self.width)

    def size(self, x_size, y_size):
        self.height=y_size
        self.width = x_size
    
    def complete(self):
        self.but.pack()

    def command(self, command):
        self.but.config(command=command)

    
            
def change_color(update_config_attr):
    color_info = colorchooser.askcolor()     
    if color_info[1]:  
        print('change color callback')
        update_config_attr(background = color_info[1])
        

def main():
    global devices, update_config
    root = tk.Tk()
    color='#6F6FF0'
    root.config(background=color)
    start_but = Button(root, "start", "pink")
    image = Photo(root, 'assets/logo.png')
    
    # but.complete()
    screen_width_w = root.winfo_screenwidth()
    screen_height_w = root.winfo_screenheight()
    screen_width_config=int(screen_width_w/2)
    screen_height_config=int(screen_height_w/2)
    start_but.size(400,150)



    image.place(screen_width_config/2, screen_height_config/2-100)    
    start_but.place(screen_width_config/2, screen_height_config/2+100)

    pallete_but=Button(root,"", color)
    pallete_but.image("assets/pallete.png")
    pallete_but.size(40,40)
    pallete_but.place(screen_width_config-20, 20)

    devices = [root, pallete_but.but]
    update_config_attr = lambda **kwargs: [dev.config(**kwargs) for dev in devices]
    pallete_but.command(lambda: change_color(update_config_attr))
    # change_color(update_config_attr)
    root.geometry(f"{screen_width_config}x{screen_height_config}")
    root.mainloop()
    return



if __name__ =="__main__":
    
    main()
