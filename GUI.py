import tkinter as tk
from tkinter import ttk

import MRP_TextWithScrollBars, MRP_FileTab, MRP_RenumberTab, MRP_TappingTab, MRP_EventHandler

class MRP:
    file = None
    def __init__(self):
        self.file = None
    eventlogger = MRP_EventHandler.EventHandler()
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
    file_tab = MRP_FileTab.FileTab(tabs, bg='#9C5935', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
    tabs.add(file_tab, text='FILE', state="normal")
    renumber_tab = MRP_RenumberTab.RenumberTab(tabs, bg='#C27027', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
    tabs.add(renumber_tab, text='RENUMBER', state="normal")
    tapping_tab = MRP_TappingTab.TappingTab(tabs, bg='#CE663E', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
    tabs.add(tapping_tab, text='TAPPING', state='normal')
    tabs.grid(column=0, row=0, sticky='nsew')

    @staticmethod
    def activate_text(self):
        self.eventlogger.generate('show_contents_event', 'normal')
    @staticmethod
    def store_file(payload):
        file = payload


    eventlogger.listen('file_selected', store_file)
    root.mainloop()

if __name__ == "__main__":
    M = MRP()