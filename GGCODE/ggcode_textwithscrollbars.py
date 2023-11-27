import tkinter as tk
import GGCODE.ggcode_eventhandler as ggcode_eventhandler

class TextWithScrollBars(tk.Frame):
    """
    This class will create a textbox with scrollbars.

    It also has the following methods used for updating the text in the textbox:
    update_text - initializes the textbox with the contents of the file
    update_text_renumbering_event - updates the textbox with the contents of the file after renumbering
    send_all_text - sends all text to listener 'send_all_text'
    replace_tapping_text - replaces the tapping text with the new tapping text
    clear_tags - clears all tags from the textbox
    prettier_it - prettifies the text in the textbox

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictbin_tools = {}
        self.dictbin_tapping = {}
        self.tool_seek_positions = []
        self.current_tool_position = 0
        self.current_tool_mark = None

        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        eventlog = ggcode_eventhandler.EventHandler()

        xscrollbar = tk.Scrollbar(self, orient="horizontal")
        yscrollbar = tk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(
            self,
            font=("Consolas", 13),
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set,
            state='disabled'
        )

        xscrollbar.config(command=self.text.xview)
        yscrollbar.config(command=self.text.yview)

        self.text.grid(row=0, column=0, sticky="nsew")
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar.grid(row=1, column=0, sticky="ew")

        self.text.tag_config('GCODE', foreground='red')
        self.text.tag_config('COORD', foreground='black')
        self.text.tag_config('M', foreground='green')
        self.text.tag_config('T', foreground='orange')
        self.text.tag_config('N', foreground='blue')
        self.text.tag_config('S', foreground='purple')
        self.text.tag_config('O', foreground='teal')
        self.text.tag_config('F', foreground='#DE5A27')
        self.text.tag_config('Z', foreground='brown')
        self.text.tag_config('R', foreground='gold')
        self.text.tag_config('D', foreground='magenta')
        self.text.tag_config('A', foreground='#1AA4BD')
        self.text.tag_config('B', foreground='#1A7BBD')
        self.text.tag_config('I', foreground='#1A44BD')
        self.text.tag_config('J', foreground='#5B1ABD')
        self.text.tag_config('K', foreground='#AA1ABD')
        self.text.tag_config('L', foreground='#36AD99')
        self.text.tag_config('H', foreground='#E29F55')
        self.text.tag_config('Q', foreground='#936129')
        self.text.tag_config('P', foreground='#6F9329')
        alltaglist = {'GCODE': [], 'COORD': [], 'M': [], 'N': [], 'T': [], 'O': [], 'S': [], 'F': [], 'Z': [], 'R': [],
                      'D': [], 'A': [], 'B': [], 'X': [], 'Y': [], 'I': [], 'J': [], 'K': [], 'L': [], 'H': [], 'Q': [],
                      'P': []}

        self.runonce = False

        def replace_tapping_text(payload):
            """
            This function will update the text in the textbox with the new tapping text
            :param payload:
            :return:
            """
            self.text.config(state='normal')
            tap_text = self.text.get('1.0', 'end').split('\n')
            # print(f'{tap_text=}')
            tapping_tool_mark = False
            line = 0
            while line < len(tap_text):
                if 'T' in tap_text[line] and 'M06' in tap_text[line] or 'T' in tap_text[line] and 'M6' in tap_text[line]:
                    start = tap_text[line].index('T')
                    stop = start + 1
                    while stop < len(tap_text[line]) and tap_text[line][stop].isnumeric():
                        stop += 1
                    if stop < len(tap_text[line]):
                        tool = tap_text[line][start:stop]
                    else:
                        tool = tap_text[line][start:]
                    if tool in payload.keys():
                        tapping_tool_mark = True
                        text_to_write = payload[tool][1]
                if tapping_tool_mark:
                    if 'G84' in tap_text[line] and 'G80' not in tap_text[line]:
                        while 'G80' not in tap_text[line]:
                            tap_text.pop(line)
                        internal_line = line
                        for item in text_to_write.split('\n'):
                            tap_text.insert(internal_line, item)
                            internal_line += 1
                        tapping_tool_mark = False
                line += 1


            self.text.delete('1.0', 'end')
            self.text.insert('1.0', '\n'.join(tap_text))
            prettier_it(self.text.get('1.0', 'end'))
            self.text.config(state='disabled')

        def clear_tags():
            """
            This function will clear all tags from the text box so that new tags can overwrite upon text updates.
            :return:
            """
            for key in alltaglist.keys():
                for index_value in range(len(alltaglist[key])):
                    self.text.tag_remove(key, alltaglist[key][index_value][0], alltaglist[key][index_value][1])
                alltaglist[key] = []

        def tbmethod_tsfwdseek(payload):
            """
            This function will seek out the tool number in the text box and return it.
            :return:
            """
            print(f'{self.current_tool_position=}')
            print(f'{len(self.tool_seek_positions)=}')


            if payload == 'forward':
                if self.current_tool_position + 1 > len(self.tool_seek_positions)-1:
                    self.current_tool_position = 0
                    self.text.config(state='normal')
                    self.text.see(self.tool_seek_positions[self.current_tool_position])
                    self.text.config(state='disabled')
                else:
                    self.current_tool_position += 1
                    self.text.config(state='normal')
                    self.text.see(self.tool_seek_positions[self.current_tool_position])
                    self.text.config(state='disabled')
            elif payload == 'backward':
                if self.current_tool_position - 1 < 0:
                    self.current_tool_position = len(self.tool_seek_positions)-1
                    self.text.see(self.tool_seek_positions[self.current_tool_position])
                else:
                    self.current_tool_position -= 1
                    self.text.see(self.current_tool_position)

        eventlog.listen('tool_seek_event', tbmethod_tsfwdseek)

        def activate_textbox(payload):
            """
            This function will activate textbox for editing purposes.
            :param payload:
            :return:
            """
            self.text.config(state=payload)

        eventlog.listen('activate_textbox', activate_textbox)

        def deactivate_textbox(payload):
            """
            This function will deactivate textbox for editing purposes.
            :param payload:
            :return:
            """
            self.text.config(state=payload)

        eventlog.listen('deactivate_textbox', deactivate_textbox)

        def prettier_it(msg):
            """
            This function will prettify the text in the textbox and also generates dictbin_tapping and dictbin_tools
            :param msg:
            :return: dictbin_tools, dictbin_tapping
            """
            # clear_tags() clears existing foreground color elements from textbox for rewrite
            clear_tags()
            msgtext = msg.split('\n')
            # print(msgtext)

            # This dictionary is sent to tapping_tab in an event generation
            self.dictbin_tapping = {}

            # This dictionary is sent to the tool_tab in an event generation
            self.dictbin_tools = {}
            self.tool_seek_positions = []

            # This set of work offsets is sent to workoffset_tab in an event generation
            self.listbin_workoffsets = set()

            # mark_tap is a boolean that marks the beginning of a tapping cycle and reset once G80 is found
            mark_tap = False
            tap_append = []
            last_tool = ''

            # Parse through document by indexed line soas to have the 'line' number for each line
            for line in range(len(msgtext)):
                skip_flag = False
                line_text = msgtext[line]
                # Raise tapping flag when G84 is found and making sure a tool was found prior
                if 'G84' in line_text and last_tool != 'blank':
                    mark_tap = True
                # Continues to append tapping lines until G80 is found
                if mark_tap and 'G80' not in line_text:
                    tap_append.append((line + 2, msgtext[line]))

                # Ensuring that the G80 found belongs to a tapping macro and not a 'reset modal parameters line'
                # Populates dictbin_tapping, which is sent to tapping_tab
                if 'G80' in line_text and 'G40' not in line_text and 'G17' not in line_text:
                    if 'Tap' in last_tool or 'TAP' in last_tool or 'tap' in last_tool:
                        tap_append.append((line + 2, msgtext[line]))
                        self.dictbin_tapping[last_tool if last_tool else 'blank'] = tap_append
                        tap_append = []
                        mark_tap = False
                        last_tool = ''

                if 'G154' in line_text:
                    start = line_text.index('G154')
                    stop = line_text.index('P')
                    stop = stop + 1
                    while stop < len(line_text) and line_text[stop].isnumeric():
                        stop += 1
                    if line_text[start:stop] == '':
                        continue
                    if stop < len(line_text):
                        work_offset = line_text[start:stop]
                    else:
                        work_offset = line_text[start:]
                    self.listbin_workoffsets.add(work_offset)

                # Skipping comment lines
                process_flag = True
                if '(' in line_text and ')' in line_text:
                    if line_text[0] == '(':
                        continue

                # Isolates tool information and adds to dictbin_tools
                if 'T' in line_text:
                    if 'M06' in line_text or 'M6' in line_text:
                        if '(' in line_text:
                            if line_text.index('(') < line_text.index('T'):
                                continue
                            elif 'M06' in line_text:
                                if line_text.index('M06') > line_text.index('('):
                                    continue
                            elif 'M6' in line_text:
                                if line_text.index('M6') > line_text.index('('):
                                    continue
                        tstart = msgtext[line].index('T')
                        stop = tstart + 1
                        while stop < len(msgtext[line]) and msgtext[line][stop].isnumeric():
                            stop += 1
                        if stop < len(msgtext[line]):
                            tool = msgtext[line][tstart:stop]
                        else:
                            tool = msgtext[line][tstart:]
                        self.tool_seek_positions.append(line)
                        # print(f'{tool=}')
                        if tool not in self.dictbin_tools.keys():
                            if '(' in msgtext[line]:
                                self.dictbin_tools[tool] = msgtext[line][
                                                                                  msgtext[line].index('('):msgtext[
                                                                                      line].index(')')+1]
                            elif msgtext[line-1] and '(' in msgtext[line - 1][0] and ')' in msgtext[line - 1][-1]:
                                self.dictbin_tools[tool] = msgtext[line - 1][msgtext[line-1].index('('):]
                            else:
                                self.dictbin_tools[tool] = 'No Tool Comment'

                        last_tool = msgtext[line][tstart:stop] + '-----' + self.dictbin_tools[
                            msgtext[line][tstart:stop]]

                # The following section prettifies the text in the textbox
                cursor = 0
                line_num = line + 1
                upper_case = ['G', 'M', 'T', 'N', 'S', 'O', 'F', 'Z', 'R', 'D', 'Q', 'P', 'I', 'J', 'K', 'L', 'H', 'A',
                              'B']
                start = 0
                end = 0
                try:
                    while cursor < len(line_text) and len(line_text) > 1:
                        charviewer = line_text[cursor]
                        if line_text[cursor] == ' ':
                            cursor += 1
                            continue
                        if line_text[cursor] == '(':
                            while line_text[cursor] != ')':
                                cursor += 1
                            continue
                        if line_text[cursor] in upper_case:
                            start = cursor
                            cursor += 1
                            while cursor < len(line_text):
                                if line_text[cursor].isnumeric():
                                    cursor += 1
                                elif line_text[cursor] == '.':
                                    cursor += 1
                                elif line_text[cursor] == '-':
                                    cursor += 1
                                else:
                                    break
                            end = cursor
                            if end != len(line_text):
                                chunk = msgtext[line][start:end]
                            else:
                                chunk = msgtext[line][start:]

                            cursor_add = str(line_num) + '.' + str(start)
                            endpoint_add = str(line_num) + '.' + str(end)

                            if chunk:
                                if len(chunk) > 1:
                                    if chunk[0] == 'G' and chunk[1].isnumeric():
                                        self.text.tag_add('GCODE', cursor_add, endpoint_add)
                                        alltaglist['GCODE'] += [(cursor_add, endpoint_add)]

                                        if 60 > int(chunk[1:]) > 53:
                                            self.listbin_workoffsets.add(chunk)

                                    elif 'X' in chunk or 'Y' in chunk:
                                        pass
                                    elif chunk[0] == 'M' and chunk[1].isnumeric():
                                        self.text.tag_add('M', cursor_add, endpoint_add)
                                        alltaglist['M'] += [(cursor_add, endpoint_add)]
                                    elif chunk[0] == 'N' and chunk[1].isnumeric():
                                        self.text.tag_add('N', cursor_add, endpoint_add)
                                        alltaglist['N'] += [(cursor_add, endpoint_add)]
                                    elif chunk[0] == 'T' and chunk[1].isnumeric():
                                        self.text.tag_add('T', cursor_add, endpoint_add)
                                        alltaglist['T'] += [(cursor_add, endpoint_add)]
                                    elif chunk[0] == 'O' and chunk[1].isnumeric():
                                        self.text.tag_add('O', cursor_add, endpoint_add)
                                        alltaglist['O'] += [(cursor_add, endpoint_add)]
                                    elif chunk[0] == 'S' and chunk[1].isnumeric():
                                        self.text.tag_add('S', cursor_add, endpoint_add)
                                        alltaglist['S'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'F' and chunk[1].isnumeric() or
                                          chunk[0] == 'F' and chunk[-1] == '.'):
                                        self.text.tag_add('F', cursor_add, endpoint_add)
                                        alltaglist['F'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'Z' and chunk[-1].isnumeric() or
                                          chunk[0] == 'Z' and chunk[-1] == '.'):
                                        self.text.tag_add('Z', cursor_add, endpoint_add)
                                        alltaglist['Z'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'R' and chunk[-1].isnumeric() or
                                          chunk[0] == 'R' and chunk[-1] == '.'):
                                        self.text.tag_add('R', cursor_add, endpoint_add)
                                        alltaglist['R'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'D' and chunk[-1].isnumeric() or
                                          chunk[0] == 'D' and chunk[-1] == '.'):
                                        self.text.tag_add('D', cursor_add, endpoint_add)
                                        alltaglist['D'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'A' and chunk[-1].isnumeric() or
                                          chunk[0] == 'A' and chunk[-1] == '.'):
                                        self.text.tag_add('A', cursor_add, endpoint_add)
                                        alltaglist['A'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'B' and chunk[-1].isnumeric() or
                                          chunk[0] == 'B' and chunk[-1] == '.'):
                                        self.text.tag_add('B', cursor_add, endpoint_add)
                                        alltaglist['B'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'I' and chunk[-1].isnumeric() or
                                          chunk[0] == 'I' and chunk[-1] == '.'):
                                        self.text.tag_add('I', cursor_add, endpoint_add)
                                        alltaglist['I'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'J' and chunk[-1].isnumeric() or
                                          chunk[0] == 'J' and chunk[-1] == '.'):
                                        self.text.tag_add('J', cursor_add, endpoint_add)
                                        alltaglist['J'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'K' and chunk[-1].isnumeric() or
                                          chunk[0] == 'K' and chunk[-1] == '.'):
                                        self.text.tag_add('K', cursor_add, endpoint_add)
                                        alltaglist['K'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'L' and chunk[-1].isnumeric() or
                                          chunk[0] == 'L' and chunk[-1] == '.'):
                                        self.text.tag_add('L', cursor_add, endpoint_add)
                                        alltaglist['L'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'H' and chunk[-1].isnumeric() or
                                          chunk[0] == 'H' and chunk[-1] == '.'):
                                        self.text.tag_add('H', cursor_add, endpoint_add)
                                        alltaglist['H'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'Q' and chunk[-1].isnumeric() or
                                          chunk[0] == 'Q' and chunk[-1] == '.'):
                                        self.text.tag_add('Q', cursor_add, endpoint_add)
                                        alltaglist['Q'] += [(cursor_add, endpoint_add)]
                                    elif (chunk[0] == 'P' and chunk[-1].isnumeric() or
                                          chunk[0] == 'P' and chunk[-1] == '.'):
                                        self.text.tag_add('P', cursor_add, endpoint_add)
                                        alltaglist['P'] += [(cursor_add, endpoint_add)]

                                else:
                                    break
                        cursor += 1
                    self.runonce = True
                    # print(dictbin_tools)
                    # print(f'inside prettier it: {self.dictbin_tapping=}')
                    # print(f'inside prettier it:{self.dictbin_tools=}')
                except IndexError as er:
                    print(f'Line: {line}')
                    print(f'IndexError: {msgtext[line]}')
                    print(f'Cursor: {cursor}')

            eventlog.generate('activate_tool_btns', True)

        def update_text(msg):
            """
            This function updates file_textbox with contents of chosen file
            :param msg: contents of chosen file
            :return: None
            """

            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", msg)
            self.text.config(state="disabled")
            eventlog.generate('disable_show', 'disabled')

            prettier_it(msg)
            eventlog.generate('tool_list_generated', self.dictbin_tools)

            # tapping_list_generated is listened to by tapping_tab
            eventlog.generate('tapping_list_generated', self.dictbin_tapping)

            # replace_tapping_text is generated by tapping_tab
            eventlog.listen('replace_tapping_text', replace_tapping_text)

            # workoffset_list_generated is listened to by workoffset_tab
            eventlog.generate('workoffset_list_generated', self.listbin_workoffsets)

        def re_update_text(msg):
            """
            This function updates file_textbox with contents of chosen file
            :param msg: contents of chosen file
            :return: None
            """

            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", msg)
            self.text.config(state="disabled")

            prettier_it(msg)
            eventlog.generate('tool_list_regenerated', self.dictbin_tools)

            # tapping_list_generated is listened to by tapping_tab
            eventlog.generate('tapping_list_generated', self.dictbin_tapping)

            # workoffset_list_generated is listened to by workoffset_tab
            eventlog.generate('workoffset_list_generated', self.listbin_workoffsets)

            # replace_tapping_text is generated by tapping_tab
            eventlog.listen('reg_replace_tapping_text', replace_tapping_text)

        def update_text_renumbering_event(payload):
            """
            This function updates file_textbox with contents of payload that has been renumbered.
            :param payload: 'str' of renumbered file contents
            :return:
            """
            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", payload)
            self.text.config(state="disabled")
            prettier_it(payload)

        def send_all_text(payload):
            """
            This function sends all text to the generator 'send_all_text'
            :param payload:
            :return:
            """
            start, stop, type = payload[0], payload[1], payload[2]
            alltext = self.text.get(start, stop)
            type_dict = {'workoffset': 'send_text_workoffset', 'tools': 'send_text_tools',
                         'renumber': 'send_text_renumber'}

            eventlog.generate(type_dict[type], alltext)

        def update_tooling_text(payload):
            """
            This function updates the text in the textbox with the new tooling text
            :param payload:
            :return:
            """
            self.text.config(state='normal')
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', payload)
            prettier_it(payload)
            self.text.config(state='disabled')

        eventlog.listen('re_update_text', re_update_text)
        eventlog.listen('get_text_workoffset', send_all_text)
        eventlog.listen('get_text_tools', send_all_text)
        eventlog.listen('get_text_renumbering', send_all_text)
        eventlog.listen('update_text', update_text)
        eventlog.listen('update_text_renumbering_event', update_text_renumbering_event)
        eventlog.listen('send_changes_to_file', update_tooling_text)

