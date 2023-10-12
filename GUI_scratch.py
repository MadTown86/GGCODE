import tkinter as tk
import tkinter.ttk
from tkinter import filedialog as fd
global select_file


root = tk.Tk()
mainframe = tk.Frame(root)
mainframe.grid(
    column=0,
    row=0,
    columnspan=2,
    rowspan=2
)

left_pane = tk.Frame(
    master=mainframe,
    height="600",
    width="800",
    relief='raised',
    border=5,
    borderwidth=5
)
left_pane.grid(
    column=0,
    row=0,
    rowspan=2
)

right_pane_top = tk.Frame(
    master=mainframe,
    height="400",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E8839"
)

right_pane_top.grid(
    column=1,
    row=0,
    sticky="N"
)

right_pane_top_file = tk.Frame(
    master=right_pane_top,
    height="400",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E8839"
)

file_btn = tk.ttk.Button(
    master=right_pane_top_file,
    name="Browse"
    command =
)
right_pane_top_renumber = tk.Frame(
    master=right_pane_top,
    height="400",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E6739"
)
right_pane_top_tapping = tk.Frame(
    master=right_pane_top,
    height="400",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E5339"
)
notebook = tkinter.ttk.Notebook(master=right_pane_top)
notebook.add(child=right_pane_top_file, text="FILE", state="normal")
notebook.add(child=right_pane_top_renumber, text="RENUMBER", state="normal")
notebook.add(child=right_pane_top_tapping, text="TAPPING", state="normal")
notebook.pack()

right_pane_bot = tk.Frame(
    master=mainframe,
    width="400",
    border=5,
    borderwidth=5,
    relief='flat'
)

confirm_btn = tk.ttk.Button(
    master=right_pane_bot,
    text="Confirm",
)
confirm_btn.pack()

right_pane_bot.grid(
    column=1,
    row=1,
)

# Event Handlers:
def open_file():
    global select_file
    select_file = fd.askopenfilename()
    with open(select_file, 'r') as f:
        select_file = f.read()
        select_file = select_file.split("\n")

root.mainloop()
