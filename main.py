from tkinter import *
from tkinter import ttk
 
root = Tk()
root.title("METANIT.COM")
root.geometry("300x250")
 
canvas = Canvas(bg="white", width=250, height=200)
canvas.pack(anchor=CENTER, expand=1)
 
btn = ttk.Button(text="Click")
canvas.create_window(10, 20, anchor=NW, window=btn, width=100, height=50)
 
root.mainloop()
