import tkinter as tk
import random
from tkinter import colorchooser, simpledialog

update_config_attr = lambda **kwargs: None
devices = []

def desaturate_rgb_average(rgb, amount=0.5):
    """
    Desaturate RGB by mixing with gray (average of RGB).
    
    Args:
        rgb: (R, G, B) in 0-255 range
        amount: 0-1 (0 = no change, 1 = grayscale)
    
    Returns:
        Desaturated (R, G, B)
    """
   
    
    def convert_to_hsv(rgb):
        r,g,b=rgb
        r=r/255
        g=g/255
        b=b/255
        Cmax=max(r,g,b)
        Cmin=min(r,g,b)
        delta = Cmax - Cmin
        H = 0
        if(delta == 0):
            H=H
        elif(Cmax == r):
            H = 60*((g-b)/delta)%6
        elif(Cmax == g):
            H = 60*((b-r)/delta+2)
        elif (Cmax == b):
            H = 60*((r-g)/delta+4)
        V=Cmax
        S= delta/Cmax if Cmax !=0 else 0
        return H,S,V

    def convert_to_rgb(hsv):
        (h,s,v)=hsv
        C=v*s
        Hnorm = abs(h/60%2-1)
        X=C*(1-Hnorm)
        m=v-C
        rd=0
        gd=0
        bd=0
        H=h
        if(H<60):
            rd,gd,bd = (C,X,0)    
        elif(H>=60 and H < 120):
            rd,gd,bd = (X,C, 0)
        elif(H>=120 and H < 180):
            rd,gd,bd = (0,C,X)
        elif(H>=180 and H < 240):
            rd,gd,bd = (0,X,C)
        elif(H>=240 and H < 300):
            rd,gd,bd = (X,0,C)
        elif(H>=300 and H < 360):
            rd,gd,bd = (C,0,X)
        r=(rd+m)*255
        g=(gd+m)*255
        b=(bd+m)*255
        return int(r),int(g),int(b)
    (h,s,v) = convert_to_hsv(rgb)
    s=amount*s
    (new_r, new_g, new_b)= convert_to_rgb((h,s,v))
    return (new_r, new_g, new_b)

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
        self.x = x_new - self.width/2
        self.y = y_new - self.height/2
        self.but.place(x = self.x, y = self.y , height = self.height, width = self.width)

    def size(self, x_size, y_size):
        self.height=y_size
        self.width = x_size
    
    def complete(self):
        self.but.pack()

    def position(self):
        return self.x, self.y

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
        print(f"row:{self.rows} color:{self.columns}")
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





class Windows:
    def __init__ (self):
        self.root = tk.Tk()
        self.color = Color('#6F6FF0')
        self.devices = []
        self.members = dict()
        self.rows = 6
        self.collums = 10
        self.member_color = 'black'
    # def update_color(self, color)
    #     self.color.

    def start_window(self):
    
        self.root.config(background=self.color.Color())
        start_but = Button(self.root, "start", "pink")
        start_but.command(self.open_new_window)
        image = Photo(self.root, 'assets/logo.png')
        
        screen_width_w = self.root.winfo_screenwidth()
        screen_height_w = self.root.winfo_screenheight()
        screen_width_config=int(screen_width_w/2)
        screen_height_config=int(screen_height_w/2)
        start_but.size(400,150)

        image.place(screen_width_config/2, screen_height_config/2-100)    
        start_but.place(screen_width_config/2, screen_height_config/2+100)

        pallete_but=Button(self.root, "", self.color.Color())
        pallete_but.image("assets/pallete.png")
        pallete_but.size(40,40)
        pallete_but.place(screen_width_config-20, 20)

        devices = [self.root, pallete_but.but]
        update_config_attr = lambda **kwargs: [dev.config(**kwargs) for dev in devices]
        pallete_but.command(lambda: self.color.change_color(update_config_attr))
        self.root.geometry(f"{screen_width_config}x{screen_height_config}")
        self.root.update_idletasks()
        self.devices = [start_but, pallete_but, image]

    def print_table(self, rows, collums, duty = 0.8):
        table = Table(self.root, rows, collums, duty)
        return table
        
    def width(self):
        return self.root.winfo_width()

    def height(self):
        return self.root.winfo_height()

    def get_member_coordinate(self, member):
        
        return
    
    def get_optimal_pos(self):
        if(len(self.members) ==0):
            x,y = self.member_button.position()
            return (x + 10,y+60)
        max = (0,0)
        for member in self.members.values():
            coors =  member.get_pos()
            if (max) < coors:
                max = coors
        return (coors[0], coors[1]+20)

    def delete_member(self, event):
        erasing_members = []
        for member in self.members.values():
            member.label.destroy()
            if(event.widget == member.label):
                key = f"{member.member.name}_{member.member.color.Color()}"
                print(f"erasing {key}")
                erasing_members.append(key)
                # self.members.pop(key)
                # self.update_member()
                # return
        for key in erasing_members:
            self.members.pop(key)
        self.update_member()

        

    def add_member(self):
        user_input = tk.simpledialog.askstring("Add player", "Enter your name:")
        if user_input is not None and user_input != "":
            name = user_input
            member = Member(name)
            member_label = tk.Label(self.root, text =name, bg=member.color.Color(), fg=self.member_color)
            member_label.bind("<Button-1>", self.delete_member)
            pos_x, pos_y = self.get_optimal_pos()
            member_info = MemberMetaInfo(member)
            member_info.set_pos(pos_x, pos_y)
            member_info.set_label(member_label)
            member_info.set_size(w=50, h=15)
            [w,h] = member_info.get_size()
            member_info.label.place(x = pos_x, y= pos_y, width=w, height = h)
            self.members[f"{name}_{member.color.Color()}"]= member_info
            print(f"add {name} with color {member.color.Color()} at {member_info.get_pos()[0]}, {member_info.get_pos()[1]}")
    
    def update_member(self):
        if(len(self.members) == 0):
            return
        for member_info in self.members.values():
            pos_x, pos_y = member_info.get_pos()
            member = member_info.member
            name = member.get_name()
            member_label = tk.Label(self.root, text =name, bg=member.color.Color(), fg=self.member_color)
            member_label.bind("<Button-1>", self.delete_member)
            member_info.set_label(member_label)
            [w,h] = member_info.get_size()
            member_info.label.place(x = pos_x, y= pos_y, width=w, height = h)
        
    def play_windows(self, r, c):
        table = self.print_table(rows= r, collums= c)
        table.update_color(self.root['bg'])
        color_c = Color(self.root['bg'])
        
        back_button = Button(self.root, "Main menu", color_c.Color())
        back_button.size(x_size = 100, y_size=50)
        back_button.command(lambda: (self.destroy(), self.start_window()))
        back_button.place(self.width() - 50, self.height()-25)

        member_button = Button(self.root, "Add player", color_c.Color())
        member_button.command(self.add_member)
        member_button.size(x_size = 100, y_size=50)
        member_button.place(self.width() - 50, 30)

        table.create()
        self.member_button = member_button
        self.devices=[table, back_button, member_button]

    def answers(self):
        None

    def destroy(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.update_member()  

    def open_new_window(self):
        self.destroy()
        table = self.play_windows(r=self.rows, c = self.collums)
        
        return table

    def run(self):
        self.root.mainloop()

class MemberMetaInfo:
    def __init__(self, member):
        self.member = member
        self.pos_x = 0
        self.pos_y = 0
        self.label = None
    
    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
    
    def set_size(self, w,h):
        self.width = w
        self.height = h
    
    def get_size(self):
        return (self.width, self.height)

    def get_pos(self):
        return (self.pos_x, self.pos_y)

    def set_label(self, label):
        self.label = label

class Member:
    def __init__(self, new_name):
        self.color = Color(self.random_color())
        self.name = new_name

    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        (r,g,b) = desaturate_rgb_average((r,g,b), 0.7)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def change_color(self, new_color):
        self.color = Color(new_color)

    def get_name(self):
        return self.name

def main():
    global devices, update_config
    
    window = Windows()
    window.start_window()
    window.run()   
    return



if __name__ =="__main__":
    main()
