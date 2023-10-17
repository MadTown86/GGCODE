import tkinter as tk
import MRP_EventHandler
from tkinter.font import Font
class TextWithScrollBars(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        eventlog = MRP_EventHandler.EventHandler()

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
        self.text.tag_config('R', foreground='violet')


        def update_text(msg, header: str = "- DEFAULT -"):
            """
            This function updates file_textbox with contents of chosen file
            :param msg: contents of chosen file
            :param header:
            :return: None
            """

            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", str(f'STATUS MESSAGE: {header} -> \n{msg}'))
            self.text.config(state="disabled")
            eventlog.generate('disable_show', 'disabled')

            msgtext = msg.split('\n')
            print(msgtext)
            dictbin_chunks = {'G': [], 'COORD': [], 'M': [], 'N': [], 'T': [], 'O': [], 'S': [], 'F': [], 'Z': [], 'R': []}
            dictbin_tapping = {'G84':[]}
            mark = False
            tap_append = []
            for line in range(len(msgtext)):
                if 'G84' in msgtext[line]:
                    mark = True
                if mark and 'G80' not in msgtext[line]:
                    tap_append.append((line+2, msgtext[line]))
                if 'G80' in msgtext[line]:
                    tap_append.append((line+2, msgtext[line]))
                    dictbin_tapping['G84'] = tap_append
                    mark = False
                cursor = 0
                endpoint = 0
                line_num = line + 2
                while endpoint < len(msgtext[line]):
                    if endpoint >= len(msgtext[line]):
                        break
                    elif cursor >= len(msgtext[line]):
                        break
                    elif msgtext[line][cursor] != ' ':
                        while endpoint < len(msgtext[line]) and msgtext[line][endpoint] != ' ':
                            endpoint += 1
                        chunk = msgtext[line][cursor:endpoint]
                        cursor_add = str(line_num) + '.' + str(cursor)
                        endpoint_add = str(line_num) + '.' + str(endpoint)
                        dict_addition = [(cursor_add, endpoint_add), msgtext[line][cursor:endpoint]]
                        if chunk[0] == 'G' and chunk[1].isnumeric():
                            self.text.tag_add('GCODE', cursor_add, endpoint_add)
                            dictbin_chunks['G'] += dict_addition
                        elif 'X' in chunk or 'Y' in chunk:
                            dictbin_chunks['COORD'] += dict_addition
                        elif chunk[0] == 'M' and chunk[1].isnumeric():
                            self.text.tag_add('M', cursor_add, endpoint_add)
                            dictbin_chunks['M'] += dict_addition
                        elif chunk[0] == 'N' and chunk[1].isnumeric():
                            self.text.tag_add('N', cursor_add, endpoint_add)
                            dictbin_chunks['N'] += dict_addition
                        elif chunk[0] == 'T' and chunk[1].isnumeric():
                            self.text.tag_add('T', cursor_add, endpoint_add)
                            dictbin_chunks['T'] += dict_addition
                        elif chunk[0] == 'O' and chunk[1].isnumeric():
                            self.text.tag_add('O', cursor_add, endpoint_add)
                            dictbin_chunks['O'] += dict_addition
                        elif chunk[0] == 'S' and chunk[1].isnumeric():
                            self.text.tag_add('S', cursor_add, endpoint_add)
                            dictbin_chunks['S'] += dict_addition
                        elif chunk[0] == 'F' and chunk[1].isnumeric():
                            self.text.tag_add('F', cursor_add, endpoint_add)
                            dictbin_chunks['F'] += dict_addition
                        elif chunk[0] == 'Z' and chunk[-1].isnumeric():
                            self.text.tag_add('Z', cursor_add, endpoint_add)
                            dictbin_chunks['Z'] += dict_addition
                        elif chunk[0] == 'R' and chunk[-1].isnumeric():
                            self.text.tag_add('R', cursor_add, endpoint_add)
                            dictbin_chunks['R'] += dict_addition
                        cursor = endpoint + 1
                        endpoint = cursor + 1
                    elif msgtext[cursor] == ' ':
                        cursor += 1
                        endpoint = cursor + 1
            print(dictbin_chunks)
            print(dictbin_tapping)

        eventlog.listen('update_text', update_text)