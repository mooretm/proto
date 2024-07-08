"""Playing with unittest and tkinter
"""

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.title('GUI Unit Testing Demo')
        self.geometry('300x300')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frm_Main = ttk.Frame(self)
        frm_Main.grid(row=0, column=0)

        self.mytext = tk.StringVar(value="Unittesting for GUIs!")
        ttk.Label(frm_Main, text=self.mytext.get()).grid(row=0, column=0, sticky='ew')

        btn_Submit = ttk.Button(frm_Main, text="Submit", command=self._on_submit)
        btn_Submit.grid(row=1, column=0, sticky='ew')

        # Center window
        self.center_window()


    def center_window(toplevel):
        """ Center the root window """
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        toplevel.geometry("+%d+%d" % (x, y)) 


    def _on_submit(self):
        # messagebox.showinfo(
        #     title="Information",
        #     message="This is a test message"
        # )
        self.mytext.set("Testing _on_submit")


if __name__ == "__main__":
    app = App()
    app.mainloop()
