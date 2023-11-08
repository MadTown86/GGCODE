import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import GGCODE.ggcode_textwithscrollbars as ggcode_textwithscrollbars
import GGCODE.ggcode_filetab as ggcode_filetab
import GGCODE.ggcode_renumbertab as ggcode_renumbertab
import GGCODE.ggcode_tappingtab as ggcode_tappingtab
import GGCODE.ggcode_eventhandler as ggcode_eventhandler
import GGCODE.ggcode_tooltab as ggcode_tooldata

class MRP:
    file = None
    def __init__(self):
        self.file = None
        self.eventlogger = ggcode_eventhandler.EventHandler()
        self.root = tk.Tk()
        self.root.grid_columnconfigure(0, weight=20)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.geometry('1000x1000')
        self.root.configure(bg='gray', relief='flat')
        self.root.grid_propagate(False)

        self.left_pane = tk.Frame(master=self.root, bg='#597275', relief='raised', height=1000, width=10)
        self.left_pane.grid(column=0, row=0, sticky='nsew')
        self.left_pane.grid_columnconfigure(0, weight=1)
        self.left_pane.grid_rowconfigure(0, weight=1)

        self.right_pane = tk.Frame(master=self.root, bg='#9E6A81', border=1, borderwidth=5, padx=5, pady=5, relief='raised', height=1000, width=300)
        self.right_pane.grid(column=1, row=0, sticky='nsew')
        self.right_pane.grid_rowconfigure(0, weight=1)
        self.confirm_btn = tk.Button(master=self.root, text='Confirm')
        self.confirm_btn.grid(column=1, row=1)

        self.textpane = ggcode_textwithscrollbars.TextWithScrollBars(self.left_pane, bg='#597275', relief='raised')
        self.textpane.grid(column=0, row=0, sticky='nsew')
        self.textpane.grid_rowconfigure(0, weight=1)
        self.textpane.grid_columnconfigure(0, weight=1)

        self.tabs = ttk.Notebook(self.right_pane)
        self.file_tab = ggcode_filetab.FileTab(self.tabs, bg='#9C5935', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
        self.tabs.add(self.file_tab, text='FILE', state="normal")
        self.renumber_tab = ggcode_renumbertab.RenumberTab(self.tabs, bg='#C27027', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
        self.tabs.add(self.renumber_tab, text='RENUMBER', state="normal")
        self.tapping_tab = ggcode_tappingtab.TappingTab(self.tabs, bg='#CE663E', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
        self.tabs.add(self.tapping_tab, text='TAPPING', state='normal')
        self.tool_tab = ggcode_tooldata.ToolTab(self.tabs, bg='#D98E04', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
        self.tabs.add(self.tool_tab, text='TOOL DATA', state='normal')
        self.tabs.grid(column=0, row=0, sticky='nsew')

        self.eventlogger.listen('file_selected', self.store_file)

        def confirm(event):
            text = self.textpane.text.get('1.0', 'end')
            file = fd.asksaveasfile()
            file.write(text)
            file.close()

        self.confirm_btn.bind("<Button-1>", confirm)

    def start(self):
        self.root.mainloop()







    @staticmethod
    def activate_text(self):
        self.eventlogger.generate('show_contents_event', 'normal')
    @staticmethod
    def store_file(payload):
        file = payload
