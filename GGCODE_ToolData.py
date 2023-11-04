import tkinter as tk
from tkinter.ttk import Radiobutton
from tkinter.ttk import Scrollbar
from tkinter.ttk import Combobox
import GGCODE_EventHandler

class ToolTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.grid(column=0, row=0, sticky='nsew')
        eventlog = GGCODE_EventHandler.EventHandler()
        bg_color = '#D98E04'
        tool_list = {}
        tool_type_choices = ['DRILL', 'RTAP', 'LTAP', 'ENDMILL', 'BALL', 'CHAMFER', 'SPOT', 'CENTER', 'CSINK', 'BULL',
                             'DOVE', 'RADIUS', 'TAPER', 'BORING', 'REAMER', 'ENGRAVE']


        xscrollbar = tk.Scrollbar(self, orient="horizontal")
        yscrollbar = tk.Scrollbar(self, orient="vertical")

        rowcount = 0
        self.current_toolvar = tk.IntVar()

        self.add_tcommentslbl = tk.Label(self, text='Add Tool Section - Top Of Page', justify='center')
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
        self.toolchange_lbl = tk.Label(self, text='Tool Number Change', justify='center')
        self.toolchange_lbl.grid(column=2, columnspan=2, row=rowcount, sticky='ew')
        rowcount += 1




        def add_update_options():
            nonlocal rowcount
            columncount = 0
            self.update_tool_lbl = tk.Label(self, text='Update Tool Data', justify='center', padx=5)
            self.update_tool_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.update_tool_number = tk.Label(self, text='T##', justify='center', padx=5)
            self.update_tool_number.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_tool_diameter = tk.Label(self, text='DIA', justify='center', padx=5)
            self.udpate_tool_diameter.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.update_loc = tk.Label(self, text='LOC', justify='center', padx=5)
            self.update_loc.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_flutes = tk.Label(self, text='FL', justify='center', padx=5)
            self.udpate_flutes.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.update_tool_type = tk.Label(self, text='TYPE', justify='center', padx=5)
            self.update_tool_type.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_oal = tk.Label(self, text='OAL', justify='center', padx=5)
            self.udpate_oal.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1
            self.udpate_oh = tk.Label(self, text='OH', justify='center', padx=5)
            self.udpate_oh.grid(column=columncount, row=rowcount, sticky='ew')
            columncount += 1

            self.update_tool_lbl.grid(columnspan=columncount)


            rowcount += 1
            self.update_tool_number_entry = tk.Entry(self, width=3, bg='white', justify='left')
            self.update_tool_number_entry.grid(column=0, row=rowcount, sticky='ew')
            self.update_tool_diameter_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_tool_diameter_entry.grid(column=1, row=rowcount, sticky='ew')
            self.update_loc_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_loc_entry.grid(column=2, row=rowcount, sticky='ew')
            self.update_flutes_entry = tk.Entry(self, width=2, bg='white', justify='left')
            self.update_flutes_entry.grid(column=3, row=rowcount, sticky='ew')
            self.update_tool_combobox = Combobox(self, width=10, values=tool_type_choices, state='readonly')
            self.update_tool_combobox.set('Select')
            self.update_tool_combobox.grid(column=4, row=rowcount, sticky='ew')

            self.update_oal_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_oal_entry.grid(column=5, row=rowcount, sticky='ew')
            self.update_oh_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_oh_entry.grid(column=6, row=rowcount, sticky='ew')
            rowcount += 1

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.update_tool_btn = tk.Button(self, text='Store Tool Update')
            self.update_tool_btn.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.tooltext_lbl = tk.Label(self, text='Updated Tool Info', justify='center')
            self.tooltext_lbl.grid(column=0, columnspan=columncount, row=rowcount, sticky='ew')
            rowcount += 1

            self.tooltext_box = tk.Text(self, width=50, height=10, bg='white', wrap='none',
                                        xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
            self.tooltext_box.grid(column=0, columnspan=columncount, row=rowcount, sticky='ew')

            xscrollbar.config(command=self.tooltext_box.xview)
            yscrollbar.config(command=self.tooltext_box.yview)
            xscrollbar.grid(column=0, columnspan=columncount, row=rowcount + 1, sticky='ew')
            yscrollbar.grid(column=columncount, row=rowcount, sticky='ns')
            self.tooltext_box.config(state='disabled')
            rowcount += 2

            self.update_tool_btn.bind('<Button-1>', udpate_tool_event)

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.send_changes_btn = tk.Button(self, text='Send Changes To File')
            self.send_changes_btn.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.send_changes_btn.bind('<Button-1>', send_changes_to_file)

        def send_changes_to_file(event):
            print('send_changes_to_file called')
            # Modify tool_list dictionary to concatenate the different string variables into one string
            tool_comment_dict = {}

            if not tool_list:
                self.tooltext_box.config(state='normal')
                self.tooltext_box.delete('1.0', 'end')
                self.tooltext_box.insert('end', 'No Tool Data To Send')
                self.tooltext_box.config(state='disabled')
            else:
                tool_list_text = '\n TOOL LIST:::\n'
                for key, value in tool_list.items():
                    print(f'{key=}')
                    print(f'{value=}')
                    tool_list_text += f'({key} : '
                    for key2, value2 in value.items():
                        print(f'{key2=}')
                        print(f'{value2=}')
                        tool_list_text += f'{key2}-{value2} '
                    tool_list_text += ')\n'

                else:
                    tool_list_text = None
                eventlog.generate('send_changes_to_file', (tool_list_text, tool_list))

                print(f'{tool_list_text=}')


        def add_tool_entries(payload):
            nonlocal rowcount
            for key, value in payload.items():
                btn_return_value = key[1:]
                radio_lbl = str(key) + 'label'
                self.radio_lbl = (
                    Radiobutton(self, text=key + ' ' + value, value=btn_return_value, variable=self.current_toolvar))
                self.radio_lbl.grid(column=0, row=rowcount, sticky='ew')
                self.toolchange_lbl = tk.Label(self, text='', name=str(key).lower(), justify='center', padx=5)
                self.toolchange_lbl.grid(column=2, columnspan=2, row=rowcount, sticky='ew')
                rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            add_update_options()

        def udpate_tool_event(event):
            tool_id = 'T' + str(self.current_toolvar.get())
            tool_number = self.update_tool_number_entry.get()
            if tool_id[1:] != tool_number:
                for widget in self.winfo_children():
                    if isinstance(widget, tk.Label):
                        if widget.winfo_name() == tool_id.lower():
                            widget.config(text=f'-> T{tool_number}')
            else:
                for widget in self.winfo_children():
                    if isinstance(widget, tk.Label):
                        if widget.winfo_name() == tool_id.lower():
                            widget.config(text=f'\'\' No Change \'\'')
            diameter = self.update_tool_diameter_entry.get()
            length_of_cut = self.update_loc_entry.get()
            flutes = self.update_flutes_entry.get()
            tool_type = self.update_tool_combobox.get()
            oal = self.update_oal_entry.get()
            oh = self.update_oh_entry.get()
            tool_list[tool_id] = {'T': '', 'DIA': '', 'LOC': '', 'FL': '', 'TYPE': '', 'OAL': '', 'OH': ''}

            tool_list[tool_id]['T'] = tool_number
            tool_list[tool_id]['DIA'] = diameter
            tool_list[tool_id]['LOC'] = length_of_cut
            tool_list[tool_id]['FL'] = flutes
            tool_list[tool_id]['TYPE'] = tool_type
            tool_list[tool_id]['OAL'] = oal
            tool_list[tool_id]['OH'] = oh
            self.tooltext_box.config(state='normal')
            self.tooltext_box.delete('1.0', 'end')
            for key, value in tool_list.items():
                self.tooltext_box.insert('end', f'{key} {value}\n')
            self.tooltext_box.config(state='disabled')







        eventlog.listen('tool_list_generated', add_tool_entries)