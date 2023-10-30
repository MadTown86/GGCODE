import tkinter as tk
from tkinter.ttk import Radiobutton
import GGCODE_EventHandler

class ToolTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.grid(column=0, row=0, sticky='nsew')
        eventlog = GGCODE_EventHandler.EventHandler()
        bg_color = '#D98E04'

        rowcount = 0
        current_toolvar = tk.IntVar()

        self.add_tcommentslbl = tk.Label(self, text='Add Tool Comments', justify='center')
        self.add_tcommentslbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
        self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.add_tc_checkbox = tk.Checkbutton(self, text='Add Tool Comments', variable=tk.BooleanVar())
        self.add_tc_checkbox.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
        self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.tool_list_lbl = tk.Label(self, text='Tool List', justify='center')
        self.tool_list_lbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1



        def add_update_options():
            nonlocal rowcount
            columncount = 0
            self.update_tool_lbl = tk.Label(self, text='Update Tool Data', justify='center')
            self.update_tool_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.update_tool_number = tk.Label(self, text='T##', justify='center')
            self.update_tool_number.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_tool_diameter = tk.Label(self, text='DIA', justify='center')
            self.udpate_tool_diameter.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.update_loc = tk.Label(self, text='LOC', justify='center')
            self.update_loc.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_flutes = tk.Label(self, text='FL', justify='center')
            self.udpate_flutes.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.update_tool_type = tk.Label(self, text='TYPE', justify='center')
            self.update_tool_type.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_oal = tk.Label(self, text='OAL', justify='center')
            self.udpate_oal.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_oh = tk.Label(self, text='OH', justify='center')
            self.udpate_oh.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            rowcount += 1
            self.update_tool_number_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_tool_number_entry.grid(column=0, row=rowcount, sticky='ew')
            self.update_tool_diameter_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_tool_diameter_entry.grid(column=1, row=rowcount, sticky='ew')
            self.update_loc_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_loc_entry.grid(column=2, row=rowcount, sticky='ew')
            self.update_flutes_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_flutes_entry.grid(column=3, row=rowcount, sticky='ew')
            self.update_tool_type_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_tool_type_entry.grid(column=4, row=rowcount, sticky='ew')
            self.update_oal_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_oal_entry.grid(column=5, row=rowcount, sticky='ew')
            self.update_oh_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_oh_entry.grid(column=6, row=rowcount, sticky='ew')
            rowcount += 1

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

        def add_tool_entries(payload):
            nonlocal rowcount
            count_label = 0
            for key, value in payload.items():
                btn_return_value = key[1:]
                radio_lbl = str(key) + 'label'
                self.radio_lbl = (
                    Radiobutton(self, text=key + ' ' + value, value=btn_return_value, variable=current_toolvar))
                self.radio_lbl.grid(column=0, row=rowcount, sticky='ew')
                rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            add_update_options()



        eventlog.listen('tool_list_generated', add_tool_entries)