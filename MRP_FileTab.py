import tkinter as tk
from tkinter import filedialog as fd
import MRP_EventHandler
import signal
class FileTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.rawfile = None
        eventlog = MRP_EventHandler.EventHandler()

        browse_lbl = tk.Label(self, text='Please Choose An *.NC File Or Equivalent', justify='left')
        browse_btn = tk.Button(self, text='Browse', justify='left', pady=10)
        show_contentslbl = tk.Label(self, text='Click To Show File Contents', justify='left')
        contents_btn = tk.Button(self, text='Show Contents', justify='left', pady=10, state='disabled')

        browse_lbl.grid(column=0, row=0, sticky='ew')
        browse_btn.grid(column=0, row=1, sticky='w')
        show_contentslbl.grid(column=0, row=2, sticky='ew')
        contents_btn.grid(column=0, row=3, sticky='w')
        self.grid_rowconfigure('1 2 3 4', uniform='1')
        self.grid(column=0, row=0, sticky='nsew')

        def select_file(SelectFileEvent):
            self.rawfile = fd.askopenfilename()
            if self.rawfile is not None:
                rawfile = self.rawfile
                eventlog.generate('file_selected', self, self.rawfile)

        browse_btn.bind("<Button 1>", select_file)
    def activate_content(self):
        self.contents_btn.config(state='normal')
