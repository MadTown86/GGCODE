"""
This holds the work offset tab class information for GGCODE project.
"""

import tkinter as tk
from tkinter.ttk import Scrollbar
from tkinter.ttk import Radiobutton
from collections import defaultdict

from GGCODE.ggcode_eventhandler import EventHandler as eventlog
import GGCODE.ggcode_exceptionhandler as EH

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
        self.Update_lbl.grid(column=2, row=0, sticky='ew')
        canvas_rowcount += 1

        self.initialized = False
        self.radiobutton_bin = {}
        self.radiobuttonlbl_bin = {}
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
            if self.initialized:
                delete_offsetradios()
                self.offset_updatesdict = {}
                update_contents()
            for workoffset in payload:
                self.workoffsets = Radiobutton(self.canvas_frame, name='radio'+str(canvas_rowcount), text=f'{workoffset}',
                                               variable=self.workoffset_selectionvar, value=workoffset)
                self.workoffsets.grid(column=0, row=canvas_rowcount, sticky='ew')
                self.workoffsets_updatelbl = tk.Label(self.canvas_frame, name=workoffset.lower()+'lbl',
                                                      text='', justify='left')
                self.blank_lblcol = tk.Label(self.canvas_frame, text='', justify='left', bg='white', padx=5)
                self.blank_lblcol.grid(column=1, row=canvas_rowcount, sticky='ew')
                self.workoffsets_updatelbl.grid(column=2, row=canvas_rowcount, sticky='ew')
                canvas_rowcount += 1
                self.radiobuttonlbl_bin[workoffset] = self.workoffsets_updatelbl
                self.radiobutton_bin['radio'+str(canvas_rowcount)] = self.workoffsets

            # Section 3 Elements - Static : User Entry Elements
            if not self.initialized:
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
                self.update_file_btn.bind('<Button-1>', update_file)
                core_rowcount += 1

            # Set a class variable to True to indicate that this does not need to be run again
            self.initialized = True

        eventlog.listen('workoffset_list_generated', add_offsetradios)

        def delete_offsetradios():
            """
            This method will update the radio buttons for each work offset.
            :param payload:
            :return:
            """
            nonlocal canvas_rowcount
            for slave in self.canvas_frame.winfo_children():
                if slave in self.radiobutton_bin.values():
                    slave.destroy()
                    canvas_rowcount -= 1
                elif slave in self.radiobuttonlbl_bin.values():
                    slave.destroy()

        def update_offsetradiolbls(payload):
            """
            This method will update the radio buttons for each work offset.
            :param payload:
            :return:
            """
            self.radiobuttonlbl_bin[payload[0]].config(text='->' + payload[1])

        def error_msg(payload):
            """
            This method will display an error message.
            :param payload:
            :return:
            """
            self.contents_updatedicttext.config(state='normal')
            self.contents_updatedicttext.delete('1.0', 'end')
            self.contents_updatedicttext.insert('1.0', payload)
            self.contents_updatedicttext.config(state='disabled')

        def update_contents():
            """
            This method will update the contents of the text box.
            :return:
            """
            offset_updatestotext = ''
            for key in self.offset_updatesdict:
                offset_updatestotext += f'{key}: {self.offset_updatesdict[key]}\n'
            if offset_updatestotext == '':
                offset_updatestotext = 'No Updates Stored'
            self.contents_updatedicttext.config(state='normal')
            self.contents_updatedicttext.delete('1.0', 'end')
            self.contents_updatedicttext.insert('1.0', offset_updatestotext)
            self.contents_updatedicttext.config(state='disabled')

        def store_updates(event):
            """
            This method will store the updates to the work offsets and populate text box with contents.
            :param event:
            :return:
            """
            try:
                qual_goffset = ''
                current_offset = self.workoffset_selectionvar.get()
                new_goffset = self.g_offset_entry.get()
                new_pnumber = self.p_number_entry.get()
                # print(f'{current_offset=}', f'{new_goffset=}', f'{new_pnumber=}')
                if not current_offset or current_offset == '':
                    error_msg('No Work Offset Selected')
                if current_offset:
                    if not new_goffset or new_goffset == '':
                        qual_goffset = 'No Change'
                    elif new_goffset:
                        # print(f'{new_goffset[0]=}')
                        if new_goffset[0] == 'G' or new_goffset[0] == 'g':
                            if new_goffset == current_offset:
                                qual_goffset = 'No Change'
                            elif len(new_goffset) < 3:
                                error_msg('Work Offset Must Be 3 or 4 Characters Long - Ex: G54-G59 or G154 with P Number')
                            elif len(new_goffset) == 3:
                                if 54 <= int(new_goffset[1:]) <= 59:
                                    qual_goffset = 'G' + new_goffset[1:]
                            elif len(new_goffset) == 4:
                                if int(new_goffset[1:]) == 154:
                                    if new_pnumber == '':
                                        error_msg('P Number Must Be Entered with G154')
                                    elif 1 <= int(new_pnumber) <= 99:
                                        qual_goffset = 'G' + new_goffset[1:] + ' ' + 'P' + new_pnumber
                                    else:
                                        error_msg('P Number Must Be Between 1 and 99')
                        else:
                            error_msg('Work Offset Must Start with "G"')
                if qual_goffset != '':
                    self.offset_updatesdict[current_offset] = qual_goffset
                    update_offsetradiolbls((current_offset, qual_goffset))
                    update_contents()
            except EH.InvalidOffsetEntry as e:
                e.messagebox.setMsg('Invalid Offset Entry')
                e.messagebox.setStackTrace(e.__context__)
                e.messagebox.start()

        def change_lbl_update(payload):
            """
            This method will update the label to show the new work offset
            :param payload:
            :return:
            """
            for lbl in self.radiobuttonlbl_bin:
                if lbl['name'] == payload:
                    lbl.config(text=self.offset_updatesdict[payload])
                else:
                    lbl.config(text='Error')

        def update_file(event):
            """
            This method will update the file with the new work offsets.
            :param event:
            :return:
            """
            try:
                error_flag = False
                accumulated_offsets = []

                for radiobutton in self.radiobutton_bin.values():
                    accumulated_offsets.append(radiobutton['value'])

                # print(f'{accumulated_offsets=}')

                for key, value in self.offset_updatesdict.items():
                    if key in accumulated_offsets and value != 'No Change':
                        accumulated_offsets.remove(key)
                        if value not in accumulated_offsets:
                            accumulated_offsets.append(value)
                        else:
                            error_flag = True
                            error_msg('Duplicate Work Offset Entries')
                            raise EH.InvalidOffsetEntry

                if not error_flag:
                    eventlog.generate('get_text_workoffset', ('1.0', 'end', 'workoffset'))
                    eventlog.listen('workoffset_list_generated', add_offsetradios)

            except EH.InvalidOffsetEntry as e:
                accumulated_offsets = []

        def receive_current_text(payload):
            """
            This method will receive the current text from the text box. It is called when the user clicks the
            'Send Changes To File' button.

            :param payload:
            :return:
            """

            print('receive_current_text called - from ggcode_workoffsettab.py')
            self.text = payload
            split_text = self.text.split('\n')
            for line_no in range(len(split_text)):
                for org_offset, changed_offset in self.offset_updatesdict.items():
                    if changed_offset == 'No Change':
                        continue
                    if org_offset in split_text[line_no]:
                        new_line = ''
                        new_line = split_text[line_no].replace(org_offset, changed_offset)
                        split_text[line_no] = new_line
                        # print(f'UPDATED LINE FROM WORKOFFSETS: {split_text[line_no]=}')

            res_text = '\n'.join(split_text)


            eventlog.generate('re_update_text', res_text)
            # print(f'{payload=}')

        eventlog.listen('send_text_workoffset', receive_current_text)




