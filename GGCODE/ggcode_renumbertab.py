"""
Renumber Tab Class
"""
import tkinter as tk
import GGCODE.ggcode_eventhandler as ggcode_eventhandler


class RenumberTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventlog = ggcode_eventhandler.EventHandler()

        self.v = tk.StringVar(self)
        self.ren_lbl_1 = tk.Label(self, text="Please Choose One Renumber Option", justify='center')
        self.no_radio = tk.Radiobutton(self, text='No Changes', value='1', variable=self.v)
        self.remove_radio = tk.Radiobutton(self, text='Remove N Numbers', value='2', variable=self.v)
        self.renumber_radio = tk.Radiobutton(self, text='Renumber All Lines', value='3', variable=self.v)
        self.onlytools_radio = tk.Radiobutton(self, text='Only Tool Changes', value='4', variable=self.v)
        self.ren_lbl_2 = tk.Label(self, text='Enter Increment Value', justify='center')
        self.ren_lbl_3 = tk.Label(self, text='Enter Max N-Number', justify='center')
        self.ren_lbl_4 = tk.Label(self, text='Enter Starting N-Number', justify='center')
        self.increment_entry = tk.Entry(self, width=3, bg='white', justify='left')
        self.maxn_entry = tk.Entry(master=self, width=6, bg='white', justify='left')
        self.start_entry = tk.Entry(master=self, width=6, bg='white', justify='left')

        self.grid_rowconfigure('0 1 2 3 4 5 6 7 8 9 10', uniform='1')
        self.ren_lbl_1.grid(column=0, row=0, sticky='ew')
        self.no_radio.grid(column=0, row=1, sticky='w')
        self.remove_radio.grid(column=0, row=2, sticky='w')
        self.renumber_radio.grid(column=0, row=3, sticky='w')
        self.onlytools_radio.grid(column=0, row=4, sticky='w')
        self.ren_lbl_2.grid(column=0, row=5, sticky='ew')
        self.increment_entry.grid(column=0, row=6, sticky='w')
        self.ren_lbl_3.grid(column=0, row=7, sticky='ew')
        self.maxn_entry.grid(column=0, row=8, sticky='w')
        self.ren_lbl_4.grid(column=0, row=9, sticky='ew')
        self.start_entry.grid(column=0, row=10, sticky='w')
        self.grid(column=0, row=0, sticky='nsew')

        self.send_lbl = tk.Label(self, text='Click Pull Current Text In Window', justify='center')
        self.send_lbl.grid(column=0, row=11, sticky='ew')
        self.sendtofile_btn = tk.Button(self, text='Send To File')
        self.sendtofile_btn.grid(column=0, row=12, sticky='ew')
        self.grid_rowconfigure(11, uniform='1')


        def get_text(event):
            """
            This method will get the text from the text pane.
            :return: text: str
            """
            self.eventlog.generate('get_text', ('1.0', 'end'))

        def receive_all_text(payload):
            """
            This method will receive the text from the text pane.
            :param payload: str
            :return: None
            """
            self.text = payload
            print('received text')
            self.renumber_selection()

        self.sendtofile_btn.bind("<Button-1>", get_text)
        self.eventlog.listen('send_all_text', receive_all_text)

    def renumber_selection(self):
        """
        This method receives the user's choice and calls the appropriate method for changing line (N) numbers.
        :return: None
        """
        print('called renumber_selection')

        start = self.start_entry.get()
        if start == '':
            start = '10'
        maxn = self.maxn_entry.get()
        if maxn == '':
            maxn = '99999'
        increment = self.increment_entry.get()
        if increment == '':
            increment = '10'

        choice = self.v.get()
        print(f'{choice=}')
        if choice == '1':
            print('No Changes')
        elif choice == '2':
            print('Remove N Numbers')
            self.remove_numbers()
        elif choice == '3':
            print('Renumber All Lines')
            self.renumber_all(start, maxn, increment)
        elif choice == '4':
            print('Only Tool Changes')
            self.only_tools(start, maxn, increment)


    def remove_numbers(self):
        """
        This method will remove all N numbers from the gcode file.
        :return: None
        """
        return_text = ''
        split_text = self.text.split('\n')
        for line in split_text:
            cursor = 0
            endpoint = 1
            if len(line) > 1:
                if line[0] == 'N':
                    while line[endpoint].isnumeric():
                        endpoint += 1
                    if line[endpoint] == ' ':
                        endpoint += 1
                    return_text += line[endpoint:] + '\n'
                else:
                    return_text += line + '\n'
            else:
                return_text += line + '\n'
        self.eventlog.generate('update_text_renumbering_event', return_text)

    def renumber_all(self, start: str, maxn: str, increment: str):
        """
        This method will renumber all lines in the gcode file.
        :return: None
        """
        return_text = ''
        current_number = int(start)
        increment = int(increment)
        split_text = self.text.split('\n')
        for line_index in range(len(split_text)):
            current_line = split_text[line_index]
            print(f'{current_line=}')
            # print(f'{len(return_text)=}')
            leading_zero_length = len(maxn) - len(str(current_number))
            leading_zeroes = '0' * leading_zero_length

            if len(current_line) == 0:
                return_text += '\n'
                continue
            elif '%' in current_line:
                return_text += '%\n'
                continue
            elif current_line[0] == 'O':
                return_text += current_line + '\n'
                continue
            elif current_line[0] == 'N':
                if current_number <= int(maxn):
                    cursor = 0
                    endpoint = 1
                    while endpoint < len(current_line) and current_line[endpoint].isnumeric():
                        endpoint += 1
                    if current_line[endpoint] == ' ':
                        endpoint += 1
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line[endpoint:] + '\n'
                    current_number += increment
                else:
                    current_number = int(start)
                    cursor = 0
                    endpoint = 1
                    while endpoint < len(current_line) and current_line[endpoint].isnumeric():
                        endpoint += 1
                    if current_line[endpoint] == ' ':
                        endpoint += 1
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line[endpoint:] + '\n'
                    current_number += increment
            elif '(' in current_line and ')' in current_line:
                if 'M06' not in current_line and 'M6' not in current_line:
                    return_text += current_line + '\n'
                    continue
                else:
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line + '\n'
                    current_number += increment
            else:
                if current_number <= int(maxn):
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line + '\n'
                    current_number += increment
                else:
                    current_number = int(start)
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line + '\n'
                    current_number += increment
        # print('\n')
        # print('renumber all print')
        # print(f'{return_text=}')
        self.eventlog.generate('update_text_renumbering_event', return_text)


    def only_tools(self, start: str, maxn: str, increment: str):
        """
        This method will only renumber tool changes in the gcode file.
        :return: None
        """
        return_text = ''
        current_number = int(start)
        increment = int(increment)
        split_text = self.text.split('\n')
        for line_index in range(len(split_text)):
            current_line = split_text[line_index]
            leading_zero_length = len(maxn) - len(str(current_number))
            leading_zeroes = '0' * leading_zero_length
            if len(current_line) == 0:
                return_text += '\n'
                continue
            elif '%' in current_line:
                return_text += '%\n'
                continue
            elif current_line[0] == 'O':
                return_text += current_line + '\n'
                continue
            elif current_line[0] == 'N':
                cursor = 0
                endpoint = 1
                while endpoint < len(current_line) and current_line[endpoint].isnumeric():
                    endpoint += 1
                if current_line[endpoint] == ' ':
                    endpoint += 1
                if 'T' in current_line and 'M' in current_line:
                    if current_number <= int(maxn):
                        return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line[endpoint:] + '\n'
                        current_number += increment
                    else:
                        current_number = start
                        return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line[endpoint:] + '\n'
                        current_number += increment
                else:
                    return_text += current_line[endpoint:] + '\n'
            elif 'T' in current_line and 'M6' in current_line or 'M06' in current_line:
                if current_number <= int(maxn):
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line + '\n'
                    current_number += increment
                else:
                    current_number = start
                    return_text += 'N' + leading_zeroes + str(current_number) + ' ' + current_line + '\n'
                    current_number += increment
            else:
                return_text += current_line + '\n'

        self.eventlog.generate('update_text_renumbering_event', return_text)


