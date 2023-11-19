"""
This holds the work offset tab class information for GGCODE project.
"""

import tkinter as tk
from tkinter import Canvas
from tkinter.ttk import Scrollbar
from tkinter.ttk import Radiobutton
from GGCODE.ggcode_eventhandler import EventHandler as eventlog

class WoTab(tk.Frame):
    """
    This class will receive scanned work offset information from the file tab, display it, and allow the user to alter
    the work offsets as needed.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workoffsets = None
        bg_color = '#D98E04'
        self.workoffsets_lbl = tk.Label(self, text='Work Offsets Page', justify='center')
        self.workoffsets_lbl.grid(column=0, row=0, sticky='ew')
        self.grid(column=0, row=0, sticky='nsew')

        self.blank_lbl = tk.Label(self, text='', foreground=bg_color, justify='left')
        self.blank_lbl.grid(column=0, row=1, sticky='ew')

        self.yscrollbar_canvas = Scrollbar(self, orient='vertical')

        self.scrollable_frame = tk.Canvas(self, bg='white', width=600, height=200, scrollregion=(0, 0, 1000, 1000),
                                          yscrollcommand=self.yscrollbar_canvas.set)

        self.canvas_frame = tk.Frame(self.scrollable_frame, bg='white', width=1000, height=1000)
        self.scrollable_frame.create_window((0, 0), window=self.canvas_frame, anchor='nw')
        self.canvas_frame.propagate(False)
        self.scrollable_frame.grid_propagate(False)
        self.scrollable_frame.propagate(False)
        self.yscrollbar_canvas.config(command=self.scrollable_frame.yview)
        self.yscrollbar_canvas.grid(column=0, row=2, sticky='nsew')
        self.scrollable_frame.grid(column=0, row=2, sticky='nsew')
        self.canvas_frame.grid(column=0, row=2, sticky='nsew')

        self.G_Code_lbl = tk.Label(self.canvas_frame, text='Work Offset', justify='left')
        self.G_Code_lbl.grid(column=0, row=0, sticky='ew')
        self.Update_lbl = tk.Label(self.canvas_frame, text='Updated To', justify='left')
        self.Update_lbl.grid(column=1, row=0, sticky='ew')

        self.initialized = False
        self.radiobuttonlbl_bin = []
        self.offset_updatesdict = {}

        self.workoffset_selectionvar = tk.StringVar()


        def add_offsetradios(payload):
            """
            This method will add the radio buttons for each work offset.
            :param payload:
            :return:
            """
            for index_wo in range(len(payload)):
                self.workoffsets = Radiobutton(self.canvas_frame, text=f'G{payload[index_wo]}',
                                               variable=self.workoffset_selectionvar, value=payload[index_wo])
                self.workoffsets.grid(column=0, row=index_wo + 1, sticky='ew')
                self.workoffsets_updatelbl = tk.Label(self.canvas_frame, name=payload[index_wo]+'lbl',
                                                      text='', justify='left')
                self.workoffsets_updatelbl.grid(column=1, row=index_wo + 1, sticky='ew')
                self.radiobuttonlbl_bin.append(self.workoffsets_updatelbl)

            self.G_offsetlbl = tk.Label(self, text='G Offset', justify='left')
            self.G_offsetlbl.grid(column=0, row=2, sticky='ew')
            self.P_numberlbl = tk.Label(self, text='P Number', justify='left')
            self.P_numberlbl.grid(column=1, row=2, sticky='ew')
            self.g_offset_entry = tk.Entry(self)
            self.g_offset_entry.grid(column=0, row=3, sticky='ew')
            self.p_number_entry = tk.Entry(self)
            self.p_number_entry.grid(column=1, row=3, sticky='ew')

            self.blank_lbl = tk.Label(self, text='', foreground=bg_color, justify='left')
            self.blank_lbl.grid(column=0, row=4, sticky='ew')
            self.store_updates_btn = tk.Button(self, text='Update', justify='left', pady=10)
            self.store_updates_btn.grid(column=0, row=5, sticky='ew')
            self.store_updates_btn.bind('<Button-1>', store_updates)

            self.contents_updatedicttext = tk.Text(self, bg='black', fg='white')
            self.contents_updatedicttext.grid(column=0, row=6, sticky='nsew')
            self.contents_updatedicttext.grid_columnconfigure(0, weight=1)
            self.contents_updatedicttext.grid_rowconfigure(0, weight=1)
            self.contents_updatedicttext.insert('1.0', 'Updated Contents')
            self.contents_updatedicttext.config(state='disabled')

            self.blank_lbl2 = tk.Label(self, text='', foreground=bg_color, justify='left')
            self.blank_lbl2.grid(column=0, row=7, sticky='ew')

            self.update_file_btn = tk.Button(self, text='Update File', justify='left', pady=10)
            self.update_file_btn.grid(column=0, row=8, sticky='ew')

            self.initialized = True

        eventlog.listen('workoffset_list_generated', add_offsetradios)

        def update_offsetradios(payload):
            """
            This method will update the radio buttons for each work offset.
            :param payload:
            :return:
            """
            for index_wo in range(len(payload)):
                self.radiobuttonlbl_bin[index_wo].config(text=payload[index_wo])

        def update_contents():
            """
            This method will update the contents of the text box.
            :return:
            """
            offset_updatestotext = ''
            for key in self.offset_updatesdict:
                offset_updatestotext += f'{key}: {self.offset_updatesdict[key]}\n'
            self.contents_updatedicttext.config(state='normal')
            self.contents_updatedicttext.delete('1.0', 'end')
            self.contents_updatedicttext.insert('1.0', self.offset_updatesdict)
            self.contents_updatedicttext.config(state='disabled')

        def store_updates(event):
            """
            This method will store the updates to the work offsets.
            :param event:
            :return:
            """
            current_offset = self.workoffset_selectionvar.get()
            new_goffset = self.g_offset_entry.get()
            new_pnumber = self.p_number_entry.get()

            self.offset_updatesdict[current_offset] = (new_goffset, new_pnumber)
            update_contents()

        def update_file(event):
            """
            This method will update the file with the new work offsets.
            :param event:
            :return:
            """
            eventlog.listen('get_text', receive_current_text)

        def receive_current_text(payload):
            """
            This method will receive the current text from the text box. It is called when the user clicks the
            'Send Changes To File' button.

            :param payload:
            :return:
            """
            self.text = payload
            print('receive_current_text called - from ggcode_workoffsettab.py')
            # print(f'{payload=}')

        def get_text():
            """
            This method will get the text from the text box. It is called when the user clicks the 'Send Changes To File'
            :return:
            """
            print('get_text called - from ggcode_workoffsettab.py')
            eventlog.generate('get_text', ('1.0', 'end'))




