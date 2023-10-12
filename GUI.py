"""
This module houses the tkinter GUI.
"""

import tkinter as tk
import tkinter.ttk
from tkinter import ttk
from tkinter import colorchooser as ch
from tkinter import filedialog as fd
global select_file

# Root Window
window = tk.Tk()

# color Chooser class for FUN
ch.Chooser(master=window)

# Notebook for tab generation
notebook = tkinter.ttk.Notebook(window)

# File Tab Objects
file_frame = tk.Frame(
    master=window,
    name="file",
    height="400",
    width="800",
    borderwidth=5,
    relief='ridge',
    background=ch.askcolor(title="Choose Background Color", parent=window)[1]
)

# File Tab Objects for GRID
file_browse_btn = tk.Button(
    master=file_frame,
    text="Browse",
    padx=5,
    pady=5,
    state="normal"
)

file_text = tk.Text(
    master=file_frame,
    height='12',
    width=75,
    state="disabled",
    wrap="none"
)

file_contents_btn = tk.Button(
    master=file_frame,
    text="Show Conents",
    padx=5,
    pady=5,
    state="normal"
)

file_browse_lbl = ttk.Label(
    master=file_frame,
    text="Please Choose A Gcode File"
)

# File Objects Grid Placements
file_frame.grid(column=0, row=0, columnspan=2, rowspan=2)
file_browse_lbl.grid(column=1, row=0)
file_browse_btn.grid(column=1, row=1)
file_contents_btn.grid(column=0, row=0)
file_text.grid(column=0, row=1, rowspan=1)
file_frame.pack()

# Renumber Tab Objects
renumber_tab = tk.Frame(
    master=window,
    name="renumber",
    height="400",
    width="800",
    borderwidth=5,
    relief='ridge',
    background=ch.askcolor(title="Choose Tab2 Color", parent=window)[1]
)
renumber_tab.pack()

# Tapping Tab Objects
tapping_tab = tk.Frame(
    master=window,
    name='tapping',
    height="400",
    width="800",
    borderwidth=5,
    relief='ridge',
    background=ch.askcolor(title="Choose Tapping Tab Color", parent=window)[1]
)

notebook.add(child=file_frame, state="normal", text="FILE")
notebook.add(child=renumber_tab, state="normal", text="RENUMBER")
notebook.add(child=tapping_tab, state="normal", text="TAPPING")
notebook.pack()

# Event Handlers

def handle_file(event):
    global select_file
    """
    Allows user to select a file
    :param event: 
    :return: 
    """
    select_file = fd.askopenfilename()
    with open(select_file, 'r') as f:
        select_file = f.read()
        print(select_file)
        f.close()


def text_update(msg, header: str = "- DEFAULT -"):
    """
    This function updates file_textbox with contents of chosen file
    :param msg: contents of chosen file
    :param header:
    :return: None
    """
    file_text.config(state="normal")
    file_text.delete("1.0", "end")
    file_text.insert("1.0", str(f'STATUS MESSAGE: {header} -> \n{msg}'))
    file_text.config(state="disabled")


def handle_show_contents(event):
    global select_file
    """
    Shows the contents of the chosen file in the textbox
    :param event: 
    :return: 
    """
    try:
        if select_file:
            text_update(select_file)
        else:
            raise
    except:
        text_update("FIRST SELECT A FILE")


# Button Bindings
file_browse_btn.bind("<Button-1>", handle_file)
file_contents_btn.bind("<Button-1>", handle_show_contents)




if __name__ == "__main__":
    window.mainloop()