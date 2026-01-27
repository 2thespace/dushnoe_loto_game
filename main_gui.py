import tkinter as tk

class Button:

    def __init__(self, root, name, bg_color='gray'):
        self.but = tk.Button(root, text=name, background=bg_color)

        self.height=50
        self.width=50
    
    def place(self,x_new,y_new):
        self.but.place(x = x_new - self.width/2, y = y_new - self.height/2, height = self.height, width = self.width)

    def size(self, x_size, y_size):
        self.height=y_size
        self.width = x_size
    
    def complete(self):
        self.but.pack()
    

def main():
    root = tk.Tk()
    color='#0F08FF'
    root.config(background=color)
    but = Button(root, "start", "yellow")
    
    # but.complete()
    screen_width_w = root.winfo_screenwidth()
    screen_height_w = root.winfo_screenheight()
    screen_width_config=int(screen_width_w/2)
    screen_height_config=int(screen_height_w/2)
    but.size(400,150)
    but.place(screen_width_config/2, screen_height_config/2+100)

    root.geometry(f"{screen_width_config}x{screen_height_config}")
    root.mainloop()
    return



if __name__ =="__main__":
    
    main()
