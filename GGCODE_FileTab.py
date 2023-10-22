import tkinter as tk
from tkinter import filedialog as fd
import GGCODE_EventHandler
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
            self.rawfile = fd.askopenfile()
            if self.rawfile is not None:
                rawfile = self.rawfile
                eventlog.generate('file_selected', rawfile)
                eventlog.generate('show_contents_event', 'normal')

        browse_btn.bind("<Button 1>", select_file)
        def activate_content(payload):
            contents_btn.config(state=payload)

        def show_contents(Event):
            for kind in eventlog.listeners:
                print(f'{kind=}')
            if self.rawfile:
                eventlog.generate('update_text', self.rawfile.read())

        def disable_show(payload):
            contents_btn.config(state=payload)

        contents_btn.bind("<Button-1>", show_contents)
        eventlog.listen('show_contents_event', activate_content)
        eventlog.listen('disable_show', disable_show)

