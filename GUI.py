import tkinter as tk
import tkinter.ttk
from tkinter import filedialog as fd
global select_file


root = tk.Tk()
mainframe = tk.Frame(root)

mainframe.grid( column=0, row=0, columnspan=2, rowspan=2)

# View Pane Elements
left_pane = tk.Frame(
    master=mainframe,
    height="800",
    width="800",
    relief='raised',
    border=5,
    borderwidth=5
)

left_pane.grid(column=0, row=0, rowspan=2, columnspan=1, sticky='nsew')
left_pane.grid_propagate(True)

# xscrollbar = tk.Scrollbar(master=left_pane, orient='horizontal')
# xscrollbar.grid(column=0, row=1, sticky='ew')
#
# yscrollbar = tk.Scrollbar(master=left_pane)
#
# yscrollbar.grid(row=0, column=1, rowspan=2, sticky='ns')

left_pane_text = tk.Text(
    master=left_pane,
    padx=5,
    pady=4,
    # xscrollcommand=xscrollbar.set,
    # yscrollcommand=yscrollbar.set
)

left_pane_text.grid(row=0, column=0, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
# xscrollbar.config(command=left_pane_text.xview)
# yscrollbar.config(command=left_pane_text.yview)

# TAB FRAME ELEMENTS
right_pane_top = tk.Frame(
    master=mainframe,
    height="800",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E8839"
)

right_pane_top.grid(column=1, row=0)

# Tabs Handled by Notebook
notebook = tkinter.ttk.Notebook(master=right_pane_top)

right_pane_top_file = tk.Frame(
    master=notebook,
    height="800",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E8839"
)

right_pane_top_file.grid(column=0, row=0)

file_btn = tk.Button(master=right_pane_top_file, text="Browse",justify='center', padx=50, pady=50)

show_contents_btn = tk.Button(master=right_pane_top_file, text="Show Contents", justify='center', padx=50, pady=50)

file_btn.grid(column=2, row=2)

show_contents_btn.grid(column=2, row=3)

right_pane_top_renumber = tk.Frame(
    master=right_pane_top,
    height="800",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E6739"
)
right_pane_top_tapping = tk.Frame(
    master=right_pane_top,
    height="800",
    width="400",
    relief='sunken',
    border=5,
    borderwidth=5,
    bg="#9E5339"
)
notebook.add(right_pane_top_file, text="FILE", state="normal")
notebook.add(child=right_pane_top_renumber, text="RENUMBER", state="normal")
notebook.add(child=right_pane_top_tapping, text="TAPPING", state="normal")
notebook.pack(expand=True, fill='both')

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

def text_update(msg, header: str = "- DEFAULT -"):
    """
    This function updates file_textbox with contents of chosen file
    :param msg: contents of chosen file
    :param header:
    :return: None
    """
    left_pane_text.config(state="normal")
    left_pane_text.delete("1.0", "end")
    left_pane_text.insert("1.0", str(f'STATUS MESSAGE: {header} -> \n{msg}'))
    left_pane_text.config(state="disabled")

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
def open_file():
    global select_file
    select_file = fd.askopenfilename()
    with open(select_file, 'r') as f:
        select_file = f.read()
def browse_click(Event):
    open_file()

file_btn.bind("<Button-1>", browse_click)
show_contents_btn.bind("<Button-1>", handle_show_contents)

root.mainloop()
