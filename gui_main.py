import tkinter as tk
from collections import OrderedDict
from tkinter import filedialog
import os
import gui_image 
from PIL import ImageTk, Image


path = ""


def select_file(event):
    global path
    name =  filedialog.askopenfilename()
    print(name)
    path = os.path.abspath(name)
    
    path_label = tk.Label(text ="Path: "+path, font="Helvetica 14", height=2)
    path_label.grid(column=1, row=1, sticky="e")


key_history = []

def main_recog(event):
    if(path == ""): 
        path_empty_label = tk.Label(text ="Path: is empty", font="Helvetica 14", height=2)
        path_empty_label.grid(column=1, row=1, sticky="e")
    else:
        os.system("python test.py -i "+path)
        print("Image Saved")
        gui_image.show_img()


def keypress(event):
    global key_history
    key_history.append(str(event.keysym))
    key_history = list(OrderedDict.fromkeys(key_history))
    if("Shift_L" in key_history and "Escape" in key_history):
        window.destroy()


def keyReleased(event):
    key_history.pop()




window = tk.Tk()
window.configure(bg="#2c3e50")
window.columnconfigure([0,1],weight=1,minsize=250)
window.rowconfigure([0,2], weight=1, minsize=100)


dev_title = tk.Label(text="""Project by Abhiraj, Advay and Aarav""",font='Helvetica 11', fg="#f1c40f", bg="#2c3e50")
dev_title.grid(column=0, row=0, sticky="nw")

use_guide= tk.Label(text="""Browse and Select the desired image file using the Browse Button
Press the Start Button to start the facial recognition system.""", font='Helvetica 14', fg="#f1c40f", bg="#2c3e50" )
use_guide.grid(column=1, row=0, sticky="ne")

button_browse = tk.Button(text = "Browse", bg="#9b59b6", width=20, font='Helvetica 11 bold', activebackground="#8e44ad")


button1 = tk.Button(text="Start", bg="#2ecc71", width=25, font='Helvetica 11 bold')
button2 = tk.Button(text="Stop", bg="#e74c3c", width=25, font='Helvetica 11 bold')

button_browse.grid(row=1, column=0, sticky="w")
button1.grid(row=2, column=0, sticky="sw")
button2.grid(row=2, column=1,sticky="se")


button1.bind("<Button-1>", main_recog)

window.bind("<KeyPress>", keypress)
window.bind("<KeyRelease>", keyReleased)

button_browse.bind("<Button-1>", select_file)
print(path)

window.mainloop()