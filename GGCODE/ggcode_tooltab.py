
import sys
import tkinter as tk
from tkinter.ttk import Radiobutton
from tkinter.ttk import Scrollbar
from tkinter.ttk import Combobox
from tkinter import Canvas

import GGCODE.ggcode_eventhandler as ggcode_eventhandler


class ToolTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(column=0, row=0, sticky='nsew')
        eventlog = ggcode_eventhandler.EventHandler()
        bg_color = '#D98E04'
        self.tool_list = {}
        tool_type_choices = ['DRILL', 'RTAP', 'LTAP', 'SHELL', 'ENDMILL', 'BALL', 'CHAMFER', 'SPOT', 'CENTER', 'CSINK', 'BULL',
                             'DOVE', 'RADIUS', 'TAPER', 'BORING', 'REAMER', 'ENGRAVE', 'PROBE']
        self.tool_list_from_textwithscrollbars = {}
        self.text = ''

        # This will flag true when the layout is initialized the first time so it isn't run again
        self.initialize = False

        # Stores radiobuttons in a dictionary for easy access
        self.radiobuttons = {}

        # Stores radiobutton checkboxes for 'Update Tool' in a dictionary for easy access
        self.radiobutton_checkboxes = {}

        original_comments = {}

        # BooleanVar for 'Update Tool Comments' checkbox
        tool_commentvar = tk.BooleanVar()
        tool_commentvar.set(False)

        # Textbox Scrollbars
        xscrollbar = Scrollbar(self, orient='horizontal')
        yscrollbar = Scrollbar(self, orient='vertical')

        # Canvas Scrollbar
        yscrollbar_canvas = Scrollbar(self, orient='vertical')

        # Canvas Creation and Child Frame Creation
        self.scrollable_frame = Canvas(self, bg='white', width=500, height=200, scrollregion=(0, 0, 1000, 1000),
                                       yscrollcommand=yscrollbar_canvas.set)
        self.canvas_frame = tk.Frame(self.scrollable_frame, bg='white', width=1000, height=1000)
        self.scrollable_frame.create_window((0, 0), window=self.canvas_frame, anchor='nw')
        self.scrollable_frame.configure(border=0, highlightthickness=0)
        self.canvas_frame.propagate(False)
        self.scrollable_frame.grid_propagate(False)
        self.scrollable_frame.propagate(False)
        yscrollbar_canvas.config(command=self.scrollable_frame.yview)

        rowcount = 0  # Row counter for grid layout, main self.frame GGCODE_ToolData
        # FIRST SECTION - Add Tool Section - GUI Elements
        header_commentvar = tk.BooleanVar() # Booleon selection for checkbox
        header_commentvar.set(False)
        self.add_tcommentslbl = tk.Label(self, text='Add Tool Section - Top Of Page', justify='center')
        self.add_tcommentslbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.add_tc_checkbox = tk.Checkbutton(self, text='Add Tool Comments', variable=header_commentvar)
        self.add_tc_checkbox.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1
        self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
        self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
        rowcount += 1

        # SECOND SECTION - Canvas Tool List, Dynamically Generated - Core GUI Elements
        self.current_toolvar = tk.IntVar()  # Currently Selected Tool RadioButton
        self.scrollable_frame.grid(column=0, columnspan=6, row=rowcount, sticky='nsew')
        yscrollbar_canvas.grid(column=6, row=rowcount, sticky='ns')
        rowcount += 1
        canvas_rowcount = 0 # Row counter for grid layout, canvas_frame
        self.tool_list_lbl = tk.Label(self.canvas_frame, text='Tool List', justify='center')
        self.tool_list_lbl.grid(row=0, column=0, sticky='ew')
        self.toolchange_lbl = tk.Label(self.canvas_frame, text='Tool Number Change', justify='center')
        self.toolchange_lbl.grid(row=0, column=2, sticky='ew')
        canvas_rowcount += 1
        rowcount += 1

        def add_gui_elements():
            """
            THIRD SECTION - Add Tool Data Update Elements
            Having this section created upon initialization removes the possibility of user trying to enter data
            before the tool list is generated.

            :return: None
            """
            nonlocal rowcount # Carry over rowcount from previous section
            columncount = 0  # Column counter for grid layout, main self.frame GGCODE_ToolData

            # Update Tool Data Section - GUI Label Elements
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

            # Update Tool Data Section - GUI Entry Elements
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

            # Store Tool Update Button - Bound to store_tool_changes
            self.update_tool_btn = tk.Button(self, text='Store Changes')
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

            # Store Tool Update Button - Bound to store_tool_changes
            self.update_tool_btn.bind("<Button-1>", store_tool_changes)
            self.update_tool_btn.bind("<Return>", store_tool_changes)

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            # Send Changes To File Button
            self.send_changes_btn = tk.Button(self, text='Send Changes To File')
            self.send_changes_btn.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1

            # Send Changes To File Button - Bound to send_changes_to_file
            self.send_changes_btn.bind('<Button-1>', send_changes_to_file)

        def receive_current_text(payload):
            """
            This method will receive the current text from the text box. It is called when the user clicks the
            'Send Changes To File' button.

            :param payload:
            :return:
            """
            self.text = payload
            print('receive_current_text called - from GGCOD_ToolData.py')
            # print(f'{payload=}')

        def get_text():
            """
            This method will get the text from the text box. It is called when the user clicks the 'Send Changes To File'
            :return:
            """
            print('get_text called - from GGCOD_ToolData.py')
            eventlog.generate('get_text_tools', ('1.0', 'end', 'tools'))

        eventlog.listen('send_text_tools', receive_current_text)

        def update_textbox_display(payload):
            """
            This method will update the text box display. It is called when the user clicks the 'Send Changes To File'
            button.

            :param payload:
            :return:
            """
            self.tooltext_box.config(state='normal')
            self.tooltext_box.delete('1.0', 'end')
            self.tooltext_box.insert('end', payload)
            self.tooltext_box.config(state='disabled')

        def send_changes_to_file(event):
            """
            This method will send the changes to the file. It is called when the user clicks the 'Send Changes To File'
            button.

            :param event:
            :return:
            """
            print('send_changes_to_file called')
            get_text()
            # Modify tool_list dictionary to concatenate the different string variables into one string
            tool_comment_dict = {}
            add_tool_list = header_commentvar.get()
            # print(f'{add_tool_list=}')
            updated_text = ''
            skip_flag = False

            check_list = [x for x in self.tool_list_from_textwithscrollbars.keys()]

            print(f'{check_list=}')

            for key, value in self.tool_list.items():
                check_list.remove(key)
                check_list.append(str('T' + value['T']))

            for tool in check_list:
                if check_list.count(tool) > 1:
                    update_textbox_display(f'Tool {tool} is listed more than once. '
                                           f'Please remove duplicates and try again.')
                    skip_flag = True
                    break

            if not skip_flag:
                if not self.tool_list:
                    update_textbox_display('No Tools Found')
                else:
                    for key, value in self.tool_list.items():
                        tool_list_text = ''
                        if value['UPDATEBOOL']:
                            for key2, value2 in value.items():
                                if value2 == '':
                                    continue
                                elif key2 == 'T':
                                    tool_list_text += f'{key2}:{value2} :'
                                elif key2 == 'UPDATEBOOL':
                                    continue
                                elif key2 == 'COMMENTS':
                                    continue
                                else:
                                    tool_list_text += f'{key2}-{value2} '
                            tool_list_text += ')'
                            tool_comment_dict[key] = tool_list_text
                        else:
                            if not value['T']:
                                tool_list_text += f'{key}: {value["COMMENTS"].replace("(", "").replace(")", "")}'
                                tool_list_text += ')'
                            else:
                                tool_list_text += f'T:{value["T"]} '
                                tool_list_text += f'{value["COMMENTS"].replace("(", "").replace(")", "")}'
                                tool_list_text += ')'
                            tool_comment_dict[key] = tool_list_text
                    # print(f'{tool_comment_dict=}')

                text = self.text.split('\n')
                insert_bulk_comment_flag = bool(header_commentvar.get())
                update_flag = False

                # If checkbox 'Add Tool Comments' then add tool comments
                org_len = len(text)
                for line in range(len(text)):
                    line = line + len(text) - org_len
                    if not text[line]:
                        continue
                    if text[line][0] == '(':
                        continue
                    if len(text[line]) > 0:
                        if text[line][0] == 'O' and insert_bulk_comment_flag:
                            tool_comments = '\n (**TOOL LIST**) \n'
                            for key, value in tool_comment_dict.items():
                                tool_comments += f'({value}\n'
                            tool_comments += '(** END TOOL LIST **)\n'
                            tool_comments = tool_comments.split('\n')
                            for index in range(len(tool_comments) - 1, 0, -1):
                                text.insert(line + 1, tool_comments[index])
                    if ('T' in text[line] and 'M06' in text[line] and text[line][0] != '('
                            or 'T' in text[line] and 'M6' in text[line] and text[line][0] != '('):
                        update_flag = False
                        start = text[line].index('T')
                        stop = start + 1
                        while stop < len(text[line]) and text[line][stop].isnumeric():
                            stop += 1
                        if stop < len(text[line]):
                            org_tool = text[line][start:stop]
                        else:
                            org_tool = text[line][start:]
                        if org_tool in self.tool_list.keys():
                            update_flag = True
                            text[line] = text[line][:start + 1] + self.tool_list[org_tool]['T']
                            if len(text[line - 1]) > 0 and text[line - 1][0] == '(':
                                text[line - 1] = f'({tool_comment_dict[org_tool]}'
                            elif len(text[line - 1]) > 0 and text[line - 1][0] != '(':
                                text.insert(line, f'({tool_comment_dict[org_tool]}')
                            else:
                                text.insert(line, f'({tool_comment_dict[org_tool]}')
                        else:
                            continue

                    if 'T' in text[line] and 'M06' not in text[line] and 'M6' not in text[line] and '(' not in text[line]:
                        start = text[line].index('T')
                        stop = start + 1
                        while stop < len(text[line]) and text[line][stop].isnumeric():
                            stop += 1
                        if stop < len(text[line]):
                            next_tool = text[line][start:stop]
                        else:
                            next_tool = text[line][start:]
                        # print(f'{next_tool=}')
                        # print(f'{tool_list.keys()=}')
                        if next_tool in self.tool_list.keys():
                            text[line] = text[line][:start + 1] + self.tool_list[next_tool]['T']
                        else:
                            continue

                    if update_flag:
                        if 'H' in text[line] and '(' not in text[line]:
                            hindex = text[line].index('H')
                            hend = hindex + 1
                            while hend < len(text[line]) and text[line][hend].isnumeric():
                                hend += 1
                            if hend >= len(text[line]):
                                hend -= 1
                            if self.tool_list[org_tool]['T'] != org_tool[1:]:
                                text[line] = f'{text[line][:hindex + 1]}{self.tool_list[org_tool]["T"]}{text[line][hend:]}'
                        if 'D' in text[line] and '(' not in text[line]:
                            dindex = text[line].index('D')
                            dend = dindex + 1
                            if dend == len(text[line]):
                                dend -= 1
                            while dend < len(text[line]) and text[line][dend].isnumeric():
                                dend += 1
                            if self.tool_list[org_tool]['T'] != org_tool[1:]:
                                text[line] = f'{text[line][:dindex + 1]}{self.tool_list[org_tool]["T"]}{text[line][dend:]}'



                updated_text = '\n'.join(text)
                eventlog.generate('re_update_text', updated_text)
                self.tool_list = {}
                update_textbox_display('')

        def add_tool_entries(payload):
            nonlocal rowcount
            nonlocal canvas_rowcount
            self.tool_list_from_textwithscrollbars = payload
            self.original_comments = payload
            for key, value in payload.items():
                btn_return_value = key[1:]
                radio_count = 1
                chkbox_lbl = str(key).lower() + 'chkbox'
                self.radio_lbl = (
                    Radiobutton(self.canvas_frame, text=key + ' ' + value, value=btn_return_value, variable=self.current_toolvar))
                self.radiobuttons[btn_return_value] = self.radio_lbl
                radio_count += 1
                self.radio_lbl.grid(column=0, row=canvas_rowcount, sticky='ew')
                self.toolchange_lbl = tk.Label(self.canvas_frame, text='', name=str(key).lower(), justify='center', padx=5)
                self.toolchange_lbl.grid(column=2, columnspan=2, row=canvas_rowcount, sticky='ew')
                canvas_rowcount += 1
            self.blank_lbl = tk.Label(self, text='', justify='center', background=bg_color)
            self.blank_lbl.grid(column=0, row=rowcount, sticky='ew')
            rowcount += 1
            if not self.initialize:
                add_gui_elements()
                self.initialize = True
            else:
                pass

        def update_tool_entries(payload):
            """
            This method will update the tool entry widgets when the user clicks the 'Send Changes To File' button.

            :param payload: {tool_id: tool_data}
            :return:
            """

            self.tool_list_from_textwithscrollbars = payload

            for item in self.canvas_frame.grid_slaves():
                item.destroy()
            canvas_rowcount = 0  # Row counter for grid layout, canvas_frame
            self.tool_list_lbl = tk.Label(self.canvas_frame, text='Tool List', justify='center')
            self.tool_list_lbl.grid(row=0, column=0, sticky='ew')
            self.toolchange_lbl = tk.Label(self.canvas_frame, text='Tool Number Change', justify='center')
            self.toolchange_lbl.grid(row=0, column=2, sticky='ew')
            self.update_tool_chkbxlbl = tk.Label(self.canvas_frame, text='Update Tool', justify='center')
            self.update_tool_chkbxlbl.grid(row=0, column=5, sticky='ew')
            canvas_rowcount += 1
            add_tool_entries(payload)

        def store_tool_changes(event):
            """
            Stores the users input into the tool_list dictionary.
            :param event:
            :return:
            """
            tool_number = None
            temp_tool_number = self.update_tool_number_entry.get()
            tool_id = 'T' + str(self.current_toolvar.get())

            if not tool_id or tool_id == 'T0' or tool_id == 'T':
                update_textbox_display('No Tool Radio Selected')
            else:
                if not temp_tool_number.isnumeric():
                    update_textbox_display('Tool Number Must Be Numeric - NO "T" PREFIX')
                elif 999 < int(temp_tool_number) < 1:
                    update_textbox_display('Tool Number Must Be Between 1 and 999')
                else:
                    tool_number = temp_tool_number
            if tool_number:
                if tool_id[1:] != tool_number:
                    for widget in self.canvas_frame.winfo_children():
                        if isinstance(widget, tk.Label):
                            if tool_id.lower() in widget.winfo_name() and len(tool_id.lower()) == len(widget.winfo_name()):
                                widget.config(text=f'-> T{tool_number}')
                else:
                    for widget in self.canvas_frame.winfo_children():
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
                for key in self.tool_list.keys():
                    if self.tool_list[key]['T'] == tool_number:
                        pass
                self.tool_list[tool_id] = {'T': '', 'UPDATEBOOL': False,
                                      'D': '', 'LOC': '', 'F': '', 'TYPE': '',
                                      'L': '', 'OH': '', 'COMMENTS': '', 'CR': ''}

                self.tool_list[tool_id]['T'] = tool_number
                self.tool_list[tool_id]['D'] = diameter
                self.tool_list[tool_id]['LOC'] = length_of_cut
                self.tool_list[tool_id]['F'] = flutes
                self.tool_list[tool_id]['TYPE'] = tool_type
                self.tool_list[tool_id]['L'] = oal
                self.tool_list[tool_id]['OH'] = oh
                self.tool_list[tool_id]['CR'] = cr
                if update_flag:
                    self.tool_list[tool_id]['UPDATEBOOL'] = True
                self.tool_list[tool_id]['COMMENTS'] = self.original_comments[tool_id]
                self.tooltext_box.config(state='normal')
                self.tooltext_box.delete('1.0', 'end')
                for key, value in self.tool_list.items():
                    self.tooltext_box.insert('end', f'{key} {value}\n')
                self.tooltext_box.config(state='disabled')

                # Reset all checkboxes and entry widgets
                self.update_tool_number_entry.delete(0, 'end')
                self.update_tool_number_entry.insert(0, str(int(tool_number) + 1))
                self.update_tool_diameter_entry.delete(0, 'end')
                self.update_loc_entry.delete(0, 'end')
                self.update_flutes_entry.delete(0, 'end')
                self.update_tool_combobox.set('DRILL')
                self.update_oal_entry.delete(0, 'end')
                self.update_oh_entry.delete(0, 'end')
                self.update_cr_entry.delete(0, 'end')
                self.add_tc_checkbox.deselect()

        # eventlog.listen('update_radio_lbl', update_radio_lbl)
        eventlog.listen('tool_list_regenerated', update_tool_entries)
        eventlog.listen('tool_list_generated', add_tool_entries)

