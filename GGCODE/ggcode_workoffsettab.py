"""
This holds the work offset tab class information for GGCODE project.
"""

import tkinter as tk
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
        core_rowcount = 0
        self.grid_columnconfigure(0, weight=50)
        self.grid_columnconfigure(1, weight=50)
        self.grid_columnconfigure(2, weight=0)

        # First Section Elements
        self.workoffsets_lbl = tk.Label(self, text='Work Offsets Page', justify='center')
        self.workoffsets_lbl.grid(column=0, row=core_rowcount, columnspan=3, sticky='ew')
        core_rowcount += 1

        self.blank_lbl = tk.Label(self, text='', background=bg_color, justify='left')
        self.blank_lbl.grid(column=0, row=core_rowcount, sticky='ew')
        core_rowcount += 1

        # Canvas Creation, Scrollbar Creation, Internal Frame Creation
        self.workoffset_selectionvar = tk.StringVar()
        yscrollbar_canvas = Scrollbar(self, orient='vertical')
        self.scrollable_canvas = tk.Canvas(self, bg='white', width=400, height=100, scrollregion=(0, 0, 1000, 1000),
                                           yscrollcommand=yscrollbar_canvas.set, borderwidth=0, relief='flat')
        self.canvas_frame = tk.Frame(self.scrollable_canvas, bg="white", width=1000, height=1000, borderwidth=0)
        self.scrollable_canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')
        self.scrollable_canvas.configure(border=0, highlightthickness=0)
        self.canvas_frame.propagate(False)
        self.scrollable_canvas.grid_propagate(False)
        self.scrollable_canvas.propagate(False)

        # Section 2 Elements - Grid
        yscrollbar_canvas.config(command=self.scrollable_canvas.yview)
        yscrollbar_canvas.grid(column=2, row=core_rowcount, sticky='ns')

        self.scrollable_canvas.grid(column=0, columnspan=2, row=core_rowcount, sticky='nsew')
        core_rowcount += 1

        self.blank_lbl = tk.Label(self, text='', background=bg_color, justify='left')
        self.blank_lbl.grid(column=0, row=core_rowcount, sticky='ew')
        core_rowcount += 1

        canvas_rowcount = 0
        self.G_Code_lbl = tk.Label(self.canvas_frame, text='Work Offset', justify='center')
        self.G_Code_lbl.grid(column=0, row=0, sticky='ew')
        self.Update_lbl = tk.Label(self.canvas_frame, text='Updated To', justify='center')
        self.Update_lbl.grid(column=1, row=0, sticky='ew')
        canvas_rowcount += 1

        self.initialized = False
        self.radiobuttonlbl_bin = []
        self.offset_updatesdict = {}

        def add_offsetradios(payload):
            nonlocal canvas_rowcount
            """
            This method will add the radio buttons for each work offset.
            :param payload:
            :return:
            """
            nonlocal core_rowcount
            # Canvas Fill Elements - Dynamic - Section 2 - User Selection Elements
            for workoffset in payload:
                self.workoffsets = Radiobutton(self.canvas_frame, name='radio'+str(canvas_rowcount), text=f'{workoffset}',
                                               variable=self.workoffset_selectionvar, value=workoffset)
                self.workoffsets.grid(column=0, row=canvas_rowcount, sticky='ew')
                self.workoffsets_updatelbl = tk.Label(self.canvas_frame, name=workoffset.lower()+'lbl',
                                                      text='', justify='left')
                self.blank_lblcol = tk.Label(self.canvas_frame, text='', justify='center', bg='white', padx=5)
                self.blank_lblcol.grid(column=1, row=canvas_rowcount, sticky='ew')
                self.workoffsets_updatelbl.grid(column=2, row=canvas_rowcount, sticky='ew')
                canvas_rowcount += 1
                self.radiobuttonlbl_bin.append(self.workoffsets_updatelbl)

            # Section 3 Elements - Static : User Entry Elements
            self.G_offsetlbl = tk.Label(self, text='G Offset', justify='left')
            self.G_offsetlbl.grid(column=0, row=core_rowcount, sticky='ew')
            self.P_numberlbl = tk.Label(self, text='P Number', justify='left')
            self.P_numberlbl.grid(column=1, row=core_rowcount, columnspan=2, sticky='ew')
            core_rowcount += 1

            self.g_offset_entry = tk.Entry(self)
            self.g_offset_entry.grid(column=0, row=core_rowcount, sticky='ew')
            self.p_number_entry = tk.Entry(self)
            self.p_number_entry.grid(column=1, row=core_rowcount, columnspan=2, sticky='ew')
            core_rowcount += 1

            self.blank_lbl = tk.Label(self, text='', background=bg_color, justify='left')
            self.blank_lbl.grid(column=0, row=core_rowcount, sticky='ew')
            core_rowcount += 1

            self.store_updates_btn = tk.Button(self, text='Store Changes', justify='left', pady=10)
            self.store_updates_btn.grid(column=0, row=core_rowcount, sticky='ew')
            self.store_updates_btn.bind('<Button-1>', store_updates)
            core_rowcount += 1

            self.blank_lbl = tk.Label(self, text='', background=bg_color, justify='left')
            self.blank_lbl.grid(column=0, row=core_rowcount, sticky='ew')
            core_rowcount += 1

            self.contents_lbl = tk.Label(self, text='Review Stored Changes', justify='left')
            self.contents_lbl.grid(column=0, row=core_rowcount, sticky='ew')
            core_rowcount += 1

            self.contents_updatedicttext = tk.Text(self, bg='white', fg='black', height=10, width=50)
            self.contents_updatedicttext.grid(column=0, row=core_rowcount, sticky='nsew')
            self.contents_updatedicttext.insert('1.0', 'Updated Contents')
            self.contents_updatedicttext.config(state='disabled')
            core_rowcount += 1

            self.blank_lbl2 = tk.Label(self, text='', background=bg_color, justify='left')
            self.blank_lbl2.grid(column=0, row=core_rowcount, sticky='ew')
            core_rowcount += 1

            self.update_file_btn = tk.Button(self, text='Send To File', justify='left', pady=10)
            self.update_file_btn.grid(column=0, row=core_rowcount, sticky='ew')
            core_rowcount += 1

            # Set a class variable to True to indicate that this does not need to be run again
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




