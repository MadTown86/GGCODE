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
var = tk.StringVar()
ren_rbtn_nochange = tk.Radiobutton(
                        master=renumber_tab,
                        text="NO CHANGE",
                        variable=var,
                        value=1
                    )
ren_rbtn_toolchanges = tk.Radiobutton(
                            master=renumber_tab,
                            text="ONLY NUMBER TOOL CHANGES",
                            variable=var,
                            value=2
                        )

ren_rbtn_removeall = tk.Radiobutton(
                        master=renumber_tab,
                        text="REMOVE ALL NUMBERS",
                        variable=var,
                        value=3
                    )
renumber_tab.grid(column=0, row=0, columnspan=1, rowspan=3)
ren_rbtn_removeall.grid(column=0, row=1)
ren_rbtn_toolchanges.grid(column=0, row=2)
ren_rbtn_nochange.grid(column=0, row=3)

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

# File Parsing Tool:
def file_scan():
    global select_file

    dia_dict = {"3/4,.75": .75, "1/2,.50,.5,.500": .50, "3/16,.1875": .1875, "1/8,.125": .125, "1/16,.0625": .0625}
    tool_changes = {}
    sf_lines = select_file.split("\n")
    for line_no in range(len(sf_lines)):
        if "M6" in sf_lines[line_no] or "M06" in sf_lines[line_no]:
            diameter = None
            if "(" in sf_lines[line_no-1]:
                tool_comment = sf_lines[line_no-1]
                for dia in dia_dict.keys():
                    if not diameter:
                        for x in dia.split(','):
                            if x in tool_comment[:7]:
                                diameter = dia_dict[dia]
            tool_changes[line_no] = [sf_lines[line_no], tool_comment, diameter]

    for ln, tc in tool_changes.items():
        print(f'{ln=} ::: {tc=}')


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
        f.close()
    file_scan()



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