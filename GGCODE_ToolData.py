import tkinter as tk
from tkinter.ttk import Radiobutton
from tkinter.ttk import Scrollbar
from tkinter.ttk import Combobox
from tkinter import Canvas
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
        radiobuttons = {}
        radiobutton_checkboxes = {}

        original_comments = {}

        header_commentvar = tk.BooleanVar()
        header_commentvar.set(False)

        tool_commentvar = tk.BooleanVar()
        tool_commentvar.set(False)

        self.tool_canvas = Canvas(self, width=500, height=200, bg='white', scrollregion=(0, 0, 500, 2000),
                                  xscrollcommand=xcanvasscrollbar.set, yscrollcommand=ycanvascrollbar.set)
        xcanvasscrollbar = tk.Scrollbar(self.tool_canvas, orient="horizontal")
        ycanvascrollbar = tk.Scrollbar(self.tool_canvas, orient="vertical")
        xscrollbar = tk.Scrollbar(self, orient="horizontal")
        yscrollbar = tk.Scrollbar(self, orient="vertical")


        self.tool_canvas.propagate(False)
        self.tool_canvas.grid_propagate(False)
        xcanvasscrollbar.config(command=self.tool_canvas.xview)
        xcanvasscrollbar.grid(column=0, row=1, sticky='ew')
        ycanvascrollbar.config(command=self.tool_canvas.yview)
        ycanvascrollbar.grid(column=1, row=0, sticky='ns')

        self.canvas_frame = tk.Frame(self.tool_canvas, bg='white')
        self.canvas_frame.grid(column=0, row=0, sticky='nsew')

        rowcount = 0
        self.current_toolvar = tk.IntVar()

        self.add_tcommentslbl = tk.Label(self, text='Add Tool Section - Top Of Page', justify='center')
        self.add_tcommentslbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.add_tc_checkbox = tk.Checkbutton(self, text='Add Tool Comments', variable=header_commentvar)
        self.add_tc_checkbox.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
        self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1

        canvas_rowcount = 0
        self.tool_canvas.grid(column=0, row=rowcount)
        self.tool_list_lbl = tk.Label(self.canvas_frame, text='Tool List', justify='center')
        self.tool_list_lbl.grid(column=0, row=canvas_rowcount, sticky='ew')
        self.toolchange_lbl = tk.Label(self.canvas_frame, text='Tool Number Change', justify='center')
        self.toolchange_lbl.grid(column=2, columnspan=2, row=canvas_rowcount, sticky='ew')
        self.update_tool_chkbxlbl = tk.Label(self.canvas_frame, text='Update Tool', justify='center')
        self.update_tool_chkbxlbl.grid(column=5, row=canvas_rowcount, sticky='ew')
        canvas_rowcount += 1
        rowcount += 1




        def add_update_options():
            nonlocal rowcount
            columncount = 0
            self.update_tool_lbl = tk.Label(self, text='Update Tool Data', justify='center', padx=5)
            self.update_tool_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.update_comments_checkbox = tk.Checkbutton(self, text='Update Tool Comments', variable=tool_commentvar)
            self.update_comments_checkbox.grid(column=0, row=rowcount, sticky='ew')
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
            self.cornerrad_lbl = tk.Label(self, text='CR', justify='center', padx=5)
            self.cornerrad_lbl.grid(column=columncount, row=rowcount, sticky='ew')
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
            self.update_tool_combobox.set('DRILL')
            self.update_tool_combobox.grid(column=4, row=rowcount, sticky='ew')
            self.update_oal_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_oal_entry.grid(column=5, row=rowcount, sticky='ew')
            self.update_oh_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_oh_entry.grid(column=6, row=rowcount, sticky='ew')
            self.update_cr_entry = tk.Entry(self, width=4, bg='white', justify='left')
            self.update_cr_entry.grid(column=7, row=rowcount, sticky='ew')
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

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.send_changes_btn = tk.Button(self, text='Send Changes To File')
            self.send_changes_btn.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1


            self.send_changes_btn.bind('<Button-1>', send_changes_to_file)

        def update_radio_lbl(payload):
            """
            This method will udpate the radiobutton labels and values based on the udpated tool list generated by
            the user.

            It is called automatically after the user clicks the 'Send Changes To File' button.
            :param payload: {tool_id: tool_data}
            :return:
            """

            # Loops through the generated radiobuttons by sequence number
            for key, value in radiobuttons.items():
                if 'T' + key in payload[1].keys():
                    value.config(text=f'T{payload[1]['T' + key]['T']} :: {payload[0]["T" + key][:10]}')
                    value.config(value=payload[1]['T' + key]['T'])
                else:
                    # TODO Create error handling and raise condition for 'No Tool Found' error
                    pass



        def send_changes_to_file(event):
            print('send_changes_to_file called')
            # Modify tool_list dictionary to concatenate the different string variables into one string
            tool_comment_dict = {}
            add_tool_list = header_commentvar.get()
            print(f'{add_tool_list=}')

            if not tool_list:
                self.tooltext_box.config(state='normal')
                self.tooltext_box.delete('1.0', 'end')
                self.tooltext_box.insert('end', 'No Tool Data To Send')
                self.tooltext_box.config(state='disabled')
            else:
                for key, value in tool_list.items():
                    tool_list_text = ''
                    for key2, value2 in value.items():
                        if key2 == 'T':
                            tool_list_text += f'{key2}:{value2} :'
                        tool_list_text += f'{key2}-{value2} '
                    tool_list_text += ')'
                    tool_comment_dict[key] = tool_list_text
                else:
                    tool_list_text = None

                eventlog.generate('send_changes_to_file', (tool_comment_dict, tool_list))
                # eventlog.generate('update_radio_lbl', (tool_comment_dict, tool_list))

                print(f'{tool_list_text=}')
                print(f'{tool_comment_dict=}')
                print(f'{tool_list=}')


        def add_tool_entries(payload):
            nonlocal rowcount
            nonlocal canvas_rowcount
            self.original_comments = payload
            for key, value in payload.items():
                btn_return_value = key[1:]
                radio_count = 1
                radio_lbl = str(key) + 'label'
                chkbox_lbl = str(key).lower() + 'chkbox'
                self.radio_lbl = (
                    Radiobutton(self.canvas_frame, text=key + ' ' + value, value=btn_return_value, variable=self.current_toolvar))
                radiobuttons[btn_return_value] = self.radio_lbl
                radio_count += 1
                self.radio_lbl.grid(column=0, row=canvas_rowcount, sticky='ew')
                self.toolchange_lbl = tk.Label(self.canvas_frame, text='', name=str(key).lower(), justify='center', padx=5)
                self.toolchange_lbl.grid(column=2, columnspan=2, row=canvas_rowcount, sticky='ew')
                self.update_chkbx = tk.Checkbutton(self.canvas_frame, name=chkbox_lbl, variable=tk.BooleanVar(), pady=0)
                self.update_chkbx.grid(column=5, row=canvas_rowcount, sticky='ew')
                radiobutton_checkboxes[key] = self.update_chkbx
                canvas_rowcount += 1
            ycanvascrollbar.grid(column=6, row=canvas_rowcount, sticky='ns')
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
                        if tool_id.lower() in widget.winfo_name() and len(tool_id.lower()) == len(widget.winfo_name()):
                            widget.config(text=f'-> T{tool_number}')
            else:
                for widget in self.winfo_children():
                    if isinstance(widget, tk.Label):
                        if tool_id.lower() in widget.winfo_name() and len(tool_id.lower()) == len(widget.winfo_name()):
                            widget.config(text=f'\'\' No Change \'\'')
            diameter = self.update_tool_diameter_entry.get()
            length_of_cut = self.update_loc_entry.get()
            flutes = self.update_flutes_entry.get()
            tool_type = self.update_tool_combobox.get()
            oal = self.update_oal_entry.get()
            oh = self.update_oh_entry.get()
            cr = self.update_cr_entry.get()
            update_flag = tool_commentvar.get()
            for key in tool_list.keys():
                if tool_list[key]['T'] == tool_number:
                    pass
            tool_list[tool_id] = {'T': '', 'UPDATEBOOL': False,
                                  'DIA': '', 'LOC': '', 'FL': '', 'TYPE': '',
                                  'OAL': '', 'OH': '', 'COMMENTS': '', 'CR': ''}

            tool_list[tool_id]['T'] = tool_number
            tool_list[tool_id]['DIA'] = diameter
            tool_list[tool_id]['LOC'] = length_of_cut
            tool_list[tool_id]['FL'] = flutes
            tool_list[tool_id]['TYPE'] = tool_type
            tool_list[tool_id]['OAL'] = oal
            tool_list[tool_id]['OH'] = oh
            tool_list[tool_id]['CR'] = cr
            if update_flag:
                tool_list[tool_id]['UPDATEBOOL'] = True
            tool_list[tool_id]['COMMENTS'] = self.original_comments[tool_id]
            self.tooltext_box.config(state='normal')
            self.tooltext_box.delete('1.0', 'end')
            for key, value in tool_list.items():
                self.tooltext_box.insert('end', f'{key} {value}\n')
            self.tooltext_box.config(state='disabled')






        # eventlog.listen('update_radio_lbl', update_radio_lbl)
        eventlog.listen('tool_list_generated', add_tool_entries)