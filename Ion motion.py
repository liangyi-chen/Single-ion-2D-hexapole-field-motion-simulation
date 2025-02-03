import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import json
from scipy.optimize import curve_fit
from tkinter import * 
from tkinter.filedialog import askopenfilename, asksaveasfilename

root = Tk()
root.geometry("500x400")
root.title("Hexapole Demo")

frame = Frame(root)
frame.pack()

# Define input fields
def create_label_entry(label, x, y, default):
    lbl = Label(root, text=label)
    lbl.place(x=x, y=y)
    entry = Entry(root)
    entry.place(x=x+50, y=y)
    entry.insert(END, str(default))
    return entry

fields = {
    "V0": create_label_entry("V0", 10, 10, 100000),
    "omega": create_label_entry("omega", 10, 40, 100),
    "x0": create_label_entry("x0", 10, 70, 0.05),
    "y0": create_label_entry("y0", 10, 100, 0),
    "q": create_label_entry("q", 10, 130, 1),
    "m": create_label_entry("m", 10, 160, 70),
    "h": create_label_entry("h", 10, 190, 0.008),
    "vx0": create_label_entry("vx0", 10, 220, 0.1),
    "vy0": create_label_entry("vy0", 10, 250, -0.5),
    "Endtime": create_label_entry("Endtime", 200, 40, 15)
}

def save_config():
    file_path = asksaveasfilename(defaultextension=".config", filetypes=[("Config files", "*.config"), ("All files", "*.*")])
    if not file_path:
        return
    config = {key: entry.get() for key, entry in fields.items()}
    with open(file_path, "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")

def load_config():
    file_path = askopenfilename(filetypes=[("Config files", "*.config"), ("All files", "*.*")])
    if not file_path:
        return
    with open(file_path, "r") as f:
        config = {}
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    for key, value in config.items():
        if key in fields:
            fields[key].delete(0, END)
            fields[key].insert(END, value)

def plot():
    V0 = float(fields["V0"].get())
    omega = float(fields["omega"].get())
    x0 = float(fields["x0"].get())
    y0 = float(fields["y0"].get())
    q = float(fields["q"].get())
    m = float(fields["m"].get())
    h = float(fields["h"].get())
    vx0 = float(fields["vx0"].get())
    vy0 = float(fields["vy0"].get())
    Endtime = float(fields["Endtime"].get())
    x = x0
    y = y0
    vx = vx0
    vy = vy0
    X = []
    Y = []
    t = 0.
    '''
    ax = (q/m)#*V0*np.cos(omega*t)#*((x-2)/(((x-2)**2+(y-0)**2)**1.5)+(x+1)/(((x+1)**2+(y-np.sqrt(3))**2)**1.5)+(x+1)/(((x+1)**2+(y+np.sqrt(3))**2)**1.5)-(x-1)/(((x-1)**2+(y-np.sqrt(3))**2)**1.5)-(x+2)/(((x+2)**2+(y-0)**2)**1.5)-(x-1)/(((x-1)**2+(y+np.sqrt(3))**2)**1.5))
    print ax
    '''
    # Start the loop for t
    while t < Endtime:
        ax = (q/m)*V0*np.cos(omega*t)*((x-2)/(((x-2)**2+(y-0)**2)**1.5)+(x+1)/(((x+1)**2+(y-np.sqrt(3))**2)**1.5)+(x+1)/(((x+1)**2+(y+np.sqrt(3))**2)**1.5)-(x-1)/(((x-1)**2+(y-np.sqrt(3))**2)**1.5)-(x+2)/(((x+2)**2+(y-0)**2)**1.5)-(x-1)/(((x-1)**2+(y+np.sqrt(3))**2)**1.5))
        ay = q/m*V0*np.cos(omega*t)*((y-0)/(((x-2)**2+(y-0)**2)**1.5)+(y-np.sqrt(3))/(((x+1)**2+(y-np.sqrt(3))**2)**1.5)+(y+np.sqrt(3))/(((x+1)**2+(y+np.sqrt(3))**2)**1.5)-(y-np.sqrt(3))/(((x-1)**2+(y-np.sqrt(3))**2)**1.5)-(y-0)/(((x+2)**2+(y-0)**2)**1.5)-(y+np.sqrt(3))/(((x-1)**2+(y+np.sqrt(3))**2)**1.5))
        x_half = x + h*vx/2
        y_half = y + h*vy/2
        ax_half = q/m*V0*np.cos(omega*t)*((x_half-2)/(((x_half-2)**2+(y_half-0)**2)**1.5)+(x_half+1)/(((x_half+1)**2+(y_half-np.sqrt(3))**2)**1.5)+(x_half+1)/(((x_half+1)**2+(y_half+np.sqrt(3))**2)**1.5)-(x_half-1)/(((x_half-1)**2+(y_half-np.sqrt(3))**2)**1.5)-(x_half+2)/(((x_half+2)**2+(y_half-0)**2)**1.5)-(x_half-1)/(((x_half-1)**2+(y_half+np.sqrt(3))**2)**1.5))
        ay_half = q/m*V0*np.cos(omega*t)*((y_half-0)/(((x_half-2)**2+(y_half-0)**2)**1.5)+(y_half-np.sqrt(3))/(((x_half+1)**2+(y_half-np.sqrt(3))**2)**1.5)+(y_half+np.sqrt(3))/(((x_half+1)**2+(y_half+np.sqrt(3))**2)**1.5)-(y_half-np.sqrt(3))/(((x_half-1)**2+(y_half-np.sqrt(3))**2)**1.5)-(y_half-0)/(((x_half+2)**2+(y_half-0)**2)**1.5)-(y_half+np.sqrt(3))/(((x_half-1)**2+(y_half+np.sqrt(3))**2)**1.5))
        vx_end = vx + h*ax_half
        vy_end = vy + h*ay_half
        x = x + 0.5*(vx + vx_end)*h
        y = y + 0.5*(vy + vx_end)*h
        X = np.append(X,x)
        Y = np.append(Y,y)
        t = t+h
        vx = vx_end
        vy = vy_end

    fig1 = plt.figure(1)
    plt.plot(X,Y)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.plot([-2,-1,-1,1,1,2],[0,1.5,-1.5,1.5,-1.5,0],'o')
    plt.show()

Plot_Button = Button(root, text = 'Plot', command=plot)
Plot_Button.place(x=100, y=320)

# Create Menu
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save_config)
file_menu.add_command(label="Load", command=load_config)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()