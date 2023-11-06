import tkinter as tk
import GGCODE_EventHandler


class TextWithScrollBars(tk.Frame):
    """
    This class will create a textbox with scrollbars.

    It also has the following methods used for updating the text in the textbox:
    update_text - initializes the textbox with the contents of the file
    update_text_renumbering_event - updates the textbox with the contents of the file after renumbering
    send_all_text - sends all text to the eventlog
    replace_tapping_text - replaces the tapping text with the new tapping text
    clear_tags - clears all tags from the textbox
    prettier_it - prettifies the text in the textbox

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        eventlog = GGCODE_EventHandler.EventHandler()

        xscrollbar = tk.Scrollbar(self, orient="horizontal")
        yscrollbar = tk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(
            self,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set,
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
        self.text.tag_config('F', foreground='gray')
        self.text.tag_config('Z', foreground='brown')
        self.text.tag_config('R', foreground='gold')
        alltaglist = {'GCODE': [], 'COORD': [], 'M': [], 'N': [], 'T': [], 'O': [], 'S': [], 'F': [], 'Z': [], 'R': []}

        self.runonce = False

        def replace_tapping_text(payload):
            """
            This function will update the text in the textbox with the new tapping text
            :param payload:
            :return:
            """
            self.text.config(state='normal')
            for key in payload.keys():
                start = str(int(self.text.search(key, '1.0', 'end').split('.')[0]) + 3) + '.0'
                stop = str(int(self.text.search('G80', start, 'end').split('.')[0])) + '.0'
                self.text.delete(start, stop)

            for key, value in payload.items():
                start = str(int(self.text.search(key, '1.0', 'end').split('.')[0]) + 3) + '.0'
                self.text.insert(start, value[1])
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
            dictbin_tapping = {}

            # This dictionary is sent to the tool_tab in an event generation
            dictbin_tools = {}

            # mark_tap is a boolean that marks the beginning of a tapping cycle and reset once G80 is found
            mark_tap = False
            tap_append = []
            last_tool = ''

            # Parse through document by indexed line soas to have the 'line' number for each line
            for line in range(len(msgtext)):
                # Raise tapping flag when G84 is found and making sure a tool was found prior
                if 'G84' in msgtext[line] and last_tool != 'blank':
                    mark_tap = True
                # Continues to append tapping lines until G80 is found
                if mark_tap and 'G80' not in msgtext[line]:
                    tap_append.append((line + 2, msgtext[line]))

                # Ensuring that the G80 found belongs to a tapping macro and not a 'reset modal parameters line'
                # Populates dictbin_tapping, which is sent to tapping_tab
                if 'G80' in msgtext[line] and 'G40' not in msgtext[line] and 'G17' not in msgtext[line]:
                    if 'Tap' in last_tool or 'TAP' in last_tool or 'tap' in last_tool:
                        tap_append.append((line + 2, msgtext[line]))
                        dictbin_tapping[last_tool if last_tool else 'blank'] = tap_append
                        tap_append = []
                        mark_tap = False
                        last_tool = ''

                # Isolates tool information and adds to dictbin_tools
                if 'T' in msgtext[line]:
                    # print(f'PRETTIER T: {msgtext[line]}')
                    # print(f'{dictbin_tools=}')
                    if 'M06' in msgtext[line] or 'M6' in msgtext[line]:
                        tstart = msgtext[line].index('T')
                        stop = tstart + 1
                        while stop < len(msgtext[line]) and msgtext[line][stop].isnumeric():
                            stop += 1
                        if stop < len(msgtext[line]):
                            tool = msgtext[line][tstart:stop]
                        else:
                            tool = msgtext[line][tstart:]
                        print(f'{tool=}')
                        if '(' in msgtext[line]:
                            dictbin_tools[tool] = msgtext[line][
                                                                              msgtext[line].index('('):msgtext[
                                                                                  line].index(')')+1]
                        elif msgtext[line-1] and '(' in msgtext[line - 1][0] and ')' in msgtext[line - 1][-1]:
                            dictbin_tools[tool] = msgtext[line - 1][msgtext[line-1].index('('):]
                        else:
                            dictbin_tools[tool] = 'No Tool Comment'

                        last_tool = msgtext[line][tstart:stop] + '-----' + dictbin_tools[
                            msgtext[line][tstart:stop]]

                # Skipping comment lines
                if '(' in msgtext[line] and ')' in msgtext[line] and 'T' not in msgtext[line]:
                    continue


                # The following section prettifies the text in the textbox
                cursor = 0
                endpoint = 0
                line_num = line + 1
                while endpoint < len(msgtext[line]):
                    if endpoint >= len(msgtext[line]):
                        break
                    elif cursor >= len(msgtext[line]):
                        break
                    elif msgtext[line][cursor] != ' ' and msgtext[line][0] != '(':
                        while endpoint < len(msgtext[line]) and msgtext[line][endpoint] != ' ':
                            endpoint += 1
                        if endpoint >= len(msgtext[line]):
                            chunk = msgtext[line][cursor:]
                        else:
                            chunk = msgtext[line][cursor:endpoint]
                        if chunk != '%' and len(chunk) == 1:
                            endpoint += 1
                            if msgtext[line][endpoint].isnumeric() or msgtext[line][endpoint] == '.':
                                while endpoint < len(msgtext[line]) and msgtext[line][endpoint] != ' ':
                                    endpoint += 1
                                if endpoint >= len(msgtext[line]):
                                    chunk = msgtext[line]
                                else:
                                    chunk = msgtext[line][cursor:endpoint].replace(' ', '')
                        cursor_add = str(line_num) + '.' + str(cursor)
                        endpoint_add = str(line_num) + '.' + str(endpoint)

                        if len(chunk) > 1:
                            if chunk[0] == 'G' and chunk[1].isnumeric():
                                self.text.tag_add('GCODE', cursor_add, endpoint_add)
                                alltaglist['GCODE'] += [(cursor_add, endpoint_add)]
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
                            elif chunk[0] == 'F' and chunk[1].isnumeric() or chunk[1] == '.':
                                self.text.tag_add('F', cursor_add, endpoint_add)
                                alltaglist['F'] += [(cursor_add, endpoint_add)]
                            elif chunk[0] == 'Z' and chunk[-1].isnumeric() or chunk[1] == '.':
                                self.text.tag_add('Z', cursor_add, endpoint_add)
                                alltaglist['Z'] += [(cursor_add, endpoint_add)]
                            elif chunk[0] == 'R' and chunk[-1].isnumeric() or chunk[1] == '.':
                                self.text.tag_add('R', cursor_add, endpoint_add)
                                alltaglist['R'] += [(cursor_add, endpoint_add)]
                            cursor = endpoint + 1
                            endpoint = cursor + 1
                    elif msgtext[cursor] == ' ':
                        cursor += 1
                        endpoint = cursor + 1
                    else:
                        cursor += 1
                        endpoint = cursor + 1
                    self.runonce = True
            return dictbin_tools, dictbin_tapping

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

            dictbin_tools, dictbin_tapping = prettier_it(msg)[0], prettier_it(msg)[1]
            eventlog.generate('tool_list_generated', dictbin_tools)

            # tapping_list_generated is listened to by tapping_tab
            eventlog.generate('tapping_list_generated', dictbin_tapping)

            # replace_tapping_text is generated by tapping_tab
            eventlog.listen('replace_tapping_text', replace_tapping_text)

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
            This function sends all text to the eventlog.
            :param payload:
            :return:
            """
            start, stop = payload[0], payload[1]
            alltext = self.text.get(start, stop)
            eventlog.generate('send_all_text', alltext)

        def update_tooling_text(payload):
            """
            This function updates the text in the textbox with the new tooling text
            :param payload:
            :return:
            """
            self.text.config(state='normal')
            text = self.text.get('1.0', 'end').split('\n')
            insert_bulk_comment_flag = bool(payload[0])
            org_tool = None
            update_flag = False

            # If checkbox 'Add Tool Comments' then add tool comments
            org_len = len(text)
            for line in range(len(text)):
                line = line + len(text) - org_len
                if len(text[line]) > 0:
                    if text[line][0] == 'O' and insert_bulk_comment_flag:
                        tool_comments = '\n (**TOOL LIST**) \n'
                        for key, value in payload[0].items():
                            tool_comments += f'({value}\n'
                        tool_comments += '(** END TOOL LIST **)\n'
                        tool_comments = tool_comments.split('\n')
                        for index in range(len(tool_comments)-1, 0, -1):
                            text.insert(line + 1, tool_comments[index])
                if 'T' in text[line] and 'M06' in text[line] or 'M6' in text[line]:
                    update_flag = False
                    start = text[line].index('T')
                    stop = start + 1
                    while stop < len(text[line]) and text[line][stop].isnumeric():
                        stop += 1
                    if stop < len(text[line]):
                        org_tool = text[line][start:stop]
                    else:
                        org_tool = text[line][start:]
                    for tool_id in payload[1].keys():
                        if org_tool in tool_id:
                            update_flag = True
                            text[line] = text[line][:start+1] + payload[1][org_tool]['T']
                            if payload[1][org_tool]['UPDATEBOOL']:
                                if len(text[line-1]) > 0 and text[line-1][0] == '(':
                                    text[line-1] = f'({payload[0][org_tool]}'
                                elif len(text[line-1]) > 0 and text[line-1][0] != '(':
                                    text.insert(line, '\n')
                                    text.insert(line, f'({payload[0][org_tool]}')
                                else:
                                    text.insert(line, f'({payload[0][org_tool]}')
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
                    for tool_id in payload[1].keys():
                        if next_tool in tool_id:
                            text[line] = text[line][:start+1] + payload[1][next_tool]['T']
                            if payload[1][next_tool]['UPDATEBOOL']:
                                if len(text[line-1]) > 0 and text[line-1][0] == '(':
                                    text[line-1] = f'({payload[0][next_tool]}'
                                elif len(text[line-1]) > 0 and text[line-1][0] != '(':
                                    text.insert(line, '\n')
                                    text.insert(line, f'({payload[0][next_tool]}')
                                else:
                                    text.insert(line, f'({payload[0][next_tool]}')
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
                        if payload[1][org_tool]['T'] != org_tool[1:]:
                            text[line] = f'{text[line][:hindex+1]}{payload[1][org_tool]['T']}{text[line][hend:]}'
                    if 'D' in text[line] and '(' not in text[line]:
                        dindex = text[line].index('D')
                        dend = dindex + 1
                        while text[line][dend].isnumeric():
                            dend += 1
                        if payload[1][org_tool]['T'] != org_tool[1:]:
                            text[line] = f'{text[line][:dindex+1]}{payload[1][org_tool]["T"]}{text[line][dend:]}'

            updated_text = '\n'.join(text)
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', updated_text)
            prettier_it(updated_text)
            self.text.config(state='disabled')

        eventlog.listen('get_text', send_all_text)
        eventlog.listen('update_text', update_text)
        eventlog.listen('update_text_renumbering_event', update_text_renumbering_event)
        eventlog.listen('send_changes_to_file', update_tooling_text)
