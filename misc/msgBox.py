import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showwarning
from tkinter.messagebox import showinfo
from turtle import title

root = tk.Tk()
root.title("Compiler test")
root.geometry("300x300")

def showBox():
    resp = askyesno(
        title="You clicked!",
        message="Are you happy you clicked??")
    print(resp)
    if resp:
        showinfo(title="Yay!", message="You are very wise.\nStick around!")
    else:
        showwarning(title="Booo!",message="You stink.")
        root.destroy()

frmCenter = ttk.Frame(root)
frmCenter.grid(column=0, row=0, sticky='nsew')
btnClick = ttk.Button(frmCenter,text="Click Me!",command=showBox)
btnClick.grid(column=0,row=0,sticky='n')

root.mainloop()
