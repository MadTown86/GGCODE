import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import GGCODE.ggcode_eventhandler as ggcode_eventhandler
import GGCODE.ggcode_exceptionhandler as EH

class FileTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.rawfile = None
        self.bg_color = '#9C5935'
        eventlog = ggcode_eventhandler.EventHandler()

        row_count = 0

        browse_lbl = tk.Label(self, text='Please Choose An *.NC File Or Equivalent', justify='left')
        blank_lbl = tk.Label(self, text='', bg=self.bg_color, justify='left')
        browse_btn = tk.Button(self, text='Browse', justify='center')

        show_contentslbl = tk.Label(self, text='Click To Scan Document', justify='left')
        contents_btn = ttk.Button(self, text='Initial Scan', state='disabled')

        browse_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        browse_btn.grid(column=0, row=row_count, sticky='s')
        row_count += 1
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        show_contentslbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        contents_btn.grid(column=0, row=row_count, sticky='s')
        row_count += 1
        blank_lbl = tk.Label(self, text='', bg=self.bg_color, justify='left')
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        activate_tb_lbl = tk.Label(self, text='Click Activate To Allow Editing', justify='left')
        activate_tb_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        blank_lbl = tk.Label(self, text='', bg=self.bg_color, justify='left')
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        activate_textbox_btn = tk.Button(self, text='Activate Textbox', justify='left')
        activate_textbox_btn.grid(column=0, row=row_count, sticky='s')
        row_count += 1
        blank_lbl = tk.Label(self, text='', bg=self.bg_color, justify='left')
        blank_lbl.grid(column=0, row=row_count, sticky='ew')
        row_count += 1
        deactivate_textbox_btn = tk.Button(self, text='Deactivate Textbox', justify='left')
        deactivate_textbox_btn.grid(column=0, row=row_count, sticky='s')
        row_count += 1
        self.grid_rowconfigure(' '.join(str(x) for x in range(1, row_count+1)), uniform='1')
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

        def activate_textbox(event):
            eventlog.generate('activate_textbox', 'normal')

        activate_textbox_btn.bind("<Button-1>", activate_textbox)

        def deactivate_textbox(event):
            eventlog.generate('deactivate_textbox', 'disabled')

        deactivate_textbox_btn.bind("<Button-1>", deactivate_textbox)