import tkinter as tk
import GGCODE_EventHandler
from tkinter.font import Font
class TextWithScrollBars(tk.Frame):
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

        def replace_text(payload):
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
            for key in alltaglist.keys():
                for index_value in range(len(alltaglist[key])):
                    self.text.tag_remove(key, alltaglist[key][index_value][0], alltaglist[key][index_value][1])
                alltaglist[key] = []
            print(f'{alltaglist=}')

        def prettier_it(msg):
            clear_tags()
            msgtext = msg.split('\n')
            dictbin_chunks = {'G': [], 'COORD': [], 'M': [], 'N': [], 'T': [], 'O': [], 'S': [], 'F': [], 'Z': [],
                              'R': []}
            dictbin_tapping = {}
            dictbin_tools = {}
            mark_tap = False
            tap_append = []
            tool_append = []
            last_tool = ''
            add_line = ''
            for line in range(len(msgtext)):
                if 'G84' in msgtext[line] and last_tool != 'blank':
                    mark_tap = True
                if mark_tap and 'G80' not in msgtext[line]:
                    tap_append.append((line + 2, msgtext[line]))
                if 'G80' in msgtext[line] and 'G40' not in msgtext[line] and 'G17' not in msgtext[line]:
                    if 'Tap' in last_tool or 'TAP' in last_tool or 'tap' in last_tool:
                        tap_append.append((line + 2, msgtext[line]))
                        dictbin_tapping[last_tool if last_tool else 'blank'] = tap_append
                        tap_append = []
                        mark_tap = False
                        last_tool = ''
                if 'T' in msgtext[line]:
                    if 'M06' in msgtext[line] or 'M6' in msgtext[line]:
                        tstart = msgtext[line].index('T')
                        if '(' in msgtext[line]:
                            dictbin_tools[msgtext[line][tstart:tstart + 3]] = msgtext[line][
                                                                              msgtext[line].index('(') + 1:msgtext[
                                                                                  line].index(')')+1]
                        elif '(' in msgtext[line - 1]:
                            dictbin_tools[msgtext[line][tstart:tstart + 3]] = msgtext[line - 1]
                        last_tool = msgtext[line][tstart:tstart + 3] + '-----' + dictbin_tools[
                            msgtext[line][tstart:tstart + 3]]
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
                        chunk = msgtext[line][cursor:endpoint]
                        print(chunk)
                        if chunk != '%' and len(chunk) == 1:
                            endpoint += 1
                            if msgtext[line][endpoint].isnumeric() or msgtext[line][endpoint] == '.':
                                while msgtext[line][endpoint] != ' ':
                                    endpoint += 1
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
            eventlog.generate('tapping_list_generated', dictbin_tapping)
            eventlog.listen('replace_text', replace_text)

        eventlog.listen('update_text', update_text)