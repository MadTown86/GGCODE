import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import GGCODE.ggcode_eventhandler as ggcode_eventhandler
import GGCODE.ggcode_exceptionhandler as EH

class FileTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.rawfile = None
        eventlog = ggcode_eventhandler.EventHandler()

        browse_lbl = tk.Label(self, text='Please Choose An *.NC File Or Equivalent', justify='left')
        browse_btn = tk.Button(self, text='Browse', justify='left', pady=10)
        show_contentslbl = tk.Label(self, text='Click To Show File Contents', justify='left')
        contents_btn = ttk.Button(self, text='Initial Scan', state='disabled')

        browse_lbl.grid(column=0, row=0, sticky='ew')
        browse_btn.grid(column=0, row=1, sticky='w')
        show_contentslbl.grid(column=0, row=2, sticky='ew')
        contents_btn.grid(column=0, row=3, sticky='w')
        self.grid_rowconfigure('1 2 3 4', uniform='1')
        self.grid(column=0, row=0, sticky='nsew')

        def select_file(SelectFileEvent):
            """
            This method will open a file dialog and allow the user to select a file.
            :param SelectFileEvent:
            :return:
            """
            try:
                self.rawfile = fd.askopenfile()
                if self.rawfile is not None:
                    rawfile = self.rawfile
                    rawfile_tolist = rawfile.read().split('\n')
                    # print(f'{rawfile_tolist=}')
                    if '%' in rawfile_tolist[0] and '%' in rawfile_tolist[-1]:
                        eventlog.generate('file_selected', rawfile.seek(0, 0))
                        eventlog.generate('show_contents_event', 'normal')
                    else:
                        raise EH.InvalidFileFormat
            except EH.InvalidFileFormat as e:
                e.messagebox.setMsg('Invalid File Format')
                e.messagebox.setStackTrace(e.__context__)
                e.messagebox.start()


        browse_btn.bind("<Button 1>", select_file)


        def activate_content(payload):
            """
            This method will activate the contents button.
            :param payload:
            :return:
            """
            contents_btn.config(state=payload)
            contents_btn.bind("<Button-1>", show_contents)
        def show_contents(Event):
            for kind in eventlog.listeners:
                print(f'{kind=}')
            if self.rawfile:
                eventlog.generate('update_text', self.rawfile.read())
                contents_btn.state(statespec=['disabled'])

        def disable_show(payload):
            contents_btn.config(state=payload)
            contents_btn.unbind("<Button-1>")


        eventlog.listen('show_contents_event', activate_content)
        eventlog.listen('disable_show', disable_show)

