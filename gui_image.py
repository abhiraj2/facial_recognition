import tkinter as tk
from PIL import ImageTk, Image
import os


"""This one is just retarded but that is the only thing I can think of rn"""

def show_img():
    RESTART = 0
    w2 = tk.Toplevel()
    w2.configure(bg="#2c3e50")
    w2.columnconfigure(0,weight=1,minsize=250)
    w2.rowconfigure([0,1], weight=1, minsize=100)
    path = "image.jpg"
    img = ImageTk.PhotoImage(Image.open(path))

    panel = tk.Label(w2, image = img)
    panel.grid(row=0, column=0, sticky="n")

    refresh_button = tk.Button(w2, text="New Test", bg="#2ecc71", width=25, font='Helvetica 11 bold')
    refresh_button.grid(column=0, row=1, sticky="ws")
    
    refresh_button.bind("<Button-1>", lambda a:w2.destroy()) #oof lambda FLEX
        

    w2.mainloop()
    
    