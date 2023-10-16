import tkinter as tk
from tkinter import ttk

import MRP_TextWithScrollBars, MRP_FileTab, MRP_RenumberTab, MRP_TappingTab

root = tk.Tk()
root.grid_columnconfigure(0, weight=20)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.geometry('1000x1000')
root.configure(bg='gray', relief='flat')
root.grid_propagate(False)

left_pane = tk.Frame(master=root, bg='#597275', relief='raised', height=1000, width=10)
left_pane.grid(column=0, row=0, sticky='nsew')
left_pane.grid_columnconfigure(0, weight=1)
left_pane.grid_rowconfigure(0, weight=1)

right_pane = tk.Frame(master=root, bg='#9E6A81', border=1, borderwidth=5, padx=5, pady=5, relief='raised', height=1000, width=300)
right_pane.grid(column=1, row=0, sticky='nsew')
right_pane.grid_rowconfigure(0, weight=1)
confirm_btn = tk.Button(master=root, text='Confirm')
confirm_btn.grid(column=1, row=1)

textpane = MRP_TextWithScrollBars.TextWithScrollBars(left_pane, bg='#597275', relief='raised')
textpane.grid(column=0, row=0, sticky='nsew')
textpane.grid_rowconfigure(0, weight=1)
textpane.grid_columnconfigure(0, weight=1)

tabs = ttk.Notebook(right_pane)
tabs.add(MRP_FileTab.FileTab(tabs, bg='#9C5935', border=5, borderwidth=5, padx=5, pady=5, relief='flat'), text='FILE', state="normal")
tabs.add(MRP_RenumberTab.RenumberTab(tabs, bg='#C27027', border=5, borderwidth=5, padx=5, pady=5, relief='flat'), text='RENUMBER', state="normal")
tabs.add(MRP_TappingTab.TappingTab(tabs, bg='#CE663E', border=5, borderwidth=5, padx=5, pady=5, relief='flat'), text='TAPPING', state='normal')
tabs.grid(column=0, row=0, sticky='nsew')

if __name__ == "__main__":
    root.mainloop()