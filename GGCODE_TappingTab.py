import tkinter as tk


import GGCODE_EventHandler
class TappingTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        framecolor = '#CE663E'
        true_falsevar = tk.StringVar()
        depthvar = tk.StringVar()
        toolvar = tk.StringVar()
        rigid_tappingdict = {}
        tapping_lines = {}
        final_tapping_output = {}

        eventlog = MRP_EventHandler.EventHandler()
        count = 0

        final_tap_elements = {}

        self.grid(column=0, row=0, sticky='nsew')
        def add_options():
            nonlocal count
            self.tap_lbl = tk.Label(self, text="Choose Repeat Rigid Tapping Options", justify='center')
            self.taptrue_radio = tk.Radiobutton(self, text='True', value='True', variable=true_falsevar)
            self.tapfalse_radio = tk.Radiobutton(self, text='False', value='False', variable=true_falsevar)
            self.tapdepth_lbl = tk.Label(self, text='Choose Depth Increment', justify='center')
            self.tapthird_radio = tk.Radiobutton(self, text='Tap 1/3 Depth Increments', value='.33',
                                            variable=depthvar, state='normal')
            self.tapfourth_radio = tk.Radiobutton(self, text='Tap 1/4 Depth Increments', value='.25',
                                             variable=depthvar, state='normal')
            self.taphalf_radio = tk.Radiobutton(self, text='Tap 1/2 Depth Increments', value='.5',
                                           variable=depthvar, state='normal')
            self.tapfull_radio = tk.Radiobutton(self, text='Tap Full Depth', value='1.0', variable=depthvar)
            count += 1
            self.tab_spacer = tk.Label(self, text='', background=framecolor, justify='center', pady=5)
            self.tab_spacer.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            self.tap_lbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            self.taptrue_radio.grid(column=0, row=count, sticky='w')
            self.tapfalse_radio.grid(column=1, row=count, sticky='e')
            count += 1
            self.tab_spacer1 = tk.Label(self, text='', background=framecolor, justify='center', pady=5)
            self.tab_spacer1.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            self.tapdepth_lbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            self.tapfull_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            self.taphalf_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            self.tapthird_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            self.tapfourth_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1

            self.tab_spacer2 = tk.Label(self, text='', background=framecolor, justify='center', pady=5)
            self.tab_spacer2.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.confirm_choices = tk.Button(self, text='Confirm Choices', justify='center', pady=10)
            self.confirm_choices.grid(column=0, columnspan=2, row=count, sticky='ew')
            self.confirm_choices.bind("<Button-1>", confirm_choices_event)
            count += 1

            self.tab_spacer3 = tk.Label(self, text='', background=framecolor, justify='center', pady=5)
            self.tab_spacer3.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.show_tappingtext = tk.Text(self, height=10, width=50, state='disabled')
            self.show_tappingtext.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.aftertextlbl = tk.Label(self, background=framecolor, justify='center')
            self.aftertextlbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.send_button = tk.Button(self, text='Send To File', justify='center', pady=10)
            self.send_button.grid(column=0, columnspan=2, row=count, sticky='ew')
            self.send_button.bind("<Button-1>", adjust_tapping_code)
            count += 1

        def show_tappingtext_event(payload):
            rigid_tappingdict[payload[0]] = [payload[1], payload[2]]
            self.show_tappingtext.config(state='normal')
            self.show_tappingtext.delete('1.0', 'end')
            for key in rigid_tappingdict.keys():
                self.show_tappingtext.insert('end', f'{key}-----{rigid_tappingdict[key]}\n')
            self.show_tappingtext.config(state='disabled')
        def confirm_choices_event(event):
            eventlog.generate('show_tappingtext_event', [toolvar.get(), true_falsevar.get(), depthvar.get()])

        def add_tapping_elements(payload):
            nonlocal final_tap_elements
            nonlocal tapping_lines
            tapping_lines = payload
            tap_lookup = {
                '5-44'   : f'{1/44:.4f}',
                '5-40'   : f'{1/40:.4f}',
                '6-32'   : f'{1/32:.4f}',
                '8-32'   : f'{1/32:.4f}',
                '10-24'  : f'{1/24:.4f}',
                '10-32'  : f'{1/32:.4f}',
                '1/4-20' : f'{1/20:.4f}',
                '.25-20' : f'{1/20:.4f}',
                '1/4-28' : f'{1/28:.4f}',
                '.25-28' : f'{1/28:.4f}',
                '5/16-18': f'{1/18:.4f}',
                '.3125-18': f'{1/18:.4f}',
                '5/16-24': f'{1/24:.4f}',
                '.3125-24': f'{1/24:.4f}',
                '3/8-16' : f'{1/16:.4f}',
                '.375-16' : f'{1/16:.4f}',
                '3/8-24' : f'{1/24:.4f}',
                '.375-24' : f'{1/24:.4f}',
                '7/16-14': f'{1/14:.4f}',
                '.4375-14': f'{1/14:.4f}',
                '7/16-20': f'{1/20:.4f}',
                '.4375-20': f'{1/20:.4f}',
                '1/2-13' : f'{1/13:.4f}',
                '.5-13' : f'{1/13:.4f}',
                '1/2-20' : f'{1/20:.4f}',
                '.5-20' : f'{1/20:.4f}',
                '9/16-12': f'{1/12:.4f}',
                '.5625-12': f'{1/12:.4f}',
                '9/16-18': f'{1/18:.4f}',
                '.5625-18': f'{1/18:.4f}',
                '5/8-11' : f'{1/11:.4f}',
                '.625-11' : f'{1/11:.4f}',
                '5/8-18' : f'{1/18:.4f}',
                '.625-18' : f'{1/18:.4f}',
                '3/4-10' : f'{1/10:.4f}',
                '.75-10' : f'{1/10:.4f}',
                '3/4-16' : f'{1/16:.4f}',
                '.75-16' : f'{1/16:.4f}',
                '7/8-9'  : f'{1/9:.4f}',
                '.875-9'  : f'{1/9:.4f}',
                '7/8-14' : f'{1/14:.4f}',
                '.875-14' : f'{1/14:.4f}',
                '1-8'    : f'{1/8:.4f}',
                '1-12'   : f'{1/12:.4f}',
                'M2.5x.45': f'{.45*.03937:.4f}',
                'm2.5x.45': f'{.45*.03937:.4f}',
                'M3x.5'  : f'{.5*.03937:.4f}',
                'm3x.5'  : f'{.5*.03937:.4f}',
                'M3.5x.6': f'{.6*.03937:.4f}',
                'm3.5x.6': f'{.6*.03937:.4f}',
                'M4x.7'  : f'{.7*.03937:.4f}',
                'm4x.7'  : f'{.7*.03937:.4f}',
                'M5x.8'  : f'{.8*.03937:.4f}',
                'm5x.8'  : f'{.8*.03937:.4f}',
                'M6x1'   : f'{1*.03937:.4f}',
                'm6x1'   : f'{1*.03937:.4f}',
                'M7x1'   : f'{1*.03937:.4f}',
                'm7x1'   : f'{1*.03937:.4f}',
                'M8x1.25': f'{1.25*.03937:.4f}',
                'm8x1.25': f'{1.25*.03937:.4f}',
                'M10x1.5': f'{1.5*.03937:.4f}',
                'm10x1.5': f'{1.5*.03937:.4f}',
                'M12x1.75': f'{1.75*.03937:.4f}',
                'm12x1.75': f'{1.75*.03937:.4f}',
                'M14x2'  : f'{2*.03937:.4f}',
                'm14x2'  : f'{2*.03937:.4f}',
                'M16x2'  : f'{2*.03937:.4f}',
                'm16x2'  : f'{2*.03937:.4f}',
            }
            for key in payload.keys():
                keysplit = key.split('-----')
                T = keysplit[0]
                comment = keysplit[1]
                drillmacro = {'Z': [], 'R': '', 'J': '1', 'F': ''}
                drillpoints = []

                for tapsize in tap_lookup.keys():
                    if tapsize in comment:
                        drillmacro['F'] = tap_lookup[tapsize]

                for line in payload[key]:
                    code_line = line[1]
                    cursor = 0
                    endpoint = 0
                    if 'G84' in code_line:
                        while endpoint < len(code_line):
                            if code_line[cursor] != ' ':
                                while endpoint < len(code_line) and code_line[endpoint] != ' ':
                                    endpoint += 1
                                chunk = code_line[cursor:endpoint]
                                if chunk[0] == 'G':
                                    pass
                                elif chunk[0] == 'Z':
                                    drillmacro['Z'] = chunk[1:]
                                elif chunk[0] == 'R':
                                    drillmacro['R'] = chunk[1:]
                                elif chunk[0] == 'J':
                                    drillmacro['J'] = chunk[1:]
                                elif chunk[0] == 'F':
                                    pass
                            cursor = endpoint
                            endpoint = cursor + 1
                    elif 'X' in code_line or 'Y' in code_line:
                        drillpoints.append(code_line)
                    elif 'G80' in code_line:
                        final_tap_elements[T] = [comment, drillmacro, drillpoints]
                    cursor += 1
                    endpoint = cursor + 1

            nonlocal count
            self.toplabel = tk.Label(self, text='Choose Tap', justify='center')
            self.toplabel.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            for T in final_tap_elements.keys():
                radiolabel = str(T) + 'label'
                labeltext = str(T) + '-----' + final_tap_elements[T][0]
                self.radiolabel = tk.Label(self, text=labeltext, justify='left')
                self.radiolabel.grid(column=1, row=count, sticky='w')
                keyradio = str(T) + '_radio'
                self.keyradio = tk.Radiobutton(self, text=str(T), value=T, variable=toolvar)
                self.keyradio.grid(column=0, row=count, sticky='w')
                count += 1
            print(f'{final_tap_elements=}')
            print(f'{tapping_lines=}')
            add_options()

        def adjust_tapping_code(event):

            #TODO edit negative value catch for zdepth
            print(f'{rigid_tappingdict=}')
            for tool, values in rigid_tappingdict.items():
                for key, value in tapping_lines.items():
                    if tool in key:
                        start = value[0][0]
                        stop = value[0][1]

                tapping_adjustments = 'G95\n'
                if values[0] == 'True':
                    tapping_values = final_tap_elements[tool]
                    for tool_comment, values in tapping_lines.items():
                        if tool in tool_comment:
                            linesToAdjust = values

                multiplier = rigid_tappingdict[tool][1]
                print(f'{multiplier=}')
                if multiplier == '.33':
                    passes = 3
                elif multiplier == '.25':
                    passes = 4
                elif multiplier == '.5':
                    passes = 2
                elif multiplier == '1.0':
                    pass

                final_depth = float(final_tap_elements[tool][1]['Z'])

                for element in linesToAdjust:

                    second_element = element[1]
                    current_zdepth = float(f'{final_depth / passes:.4f}')
                    if 'G84' in second_element:
                        if 'X' not in second_element and 'Y' not in second_element:
                            initial_line = f'G84 Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"][0]} F{final_tap_elements[tool][1]["F"]}'
                            tapping_adjustments += initial_line + '\n'
                            current_zdepth += float(f'{final_depth / passes:.4f}')
                            while current_zdepth >= final_depth:
                                tapping_adjustments += f'G84 Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"][0]} F{final_tap_elements[tool][1]["F"]}\n'
                                current_zdepth += float(f'{final_depth / passes:.4f}')
                            continue
                        elif 'X' in second_element and 'Y' not in second_element:
                            cursor = element.index('X')
                            while second_element[cursor] != ' ':
                                cursor += 1
                            first_half = second_element[:cursor]
                            second_half = f'Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]} F{final_tap_elements[tool][1]["F"]}'
                            initial_line = first_half + second_half
                        elif 'X' not in second_element and 'Y' in second_element:
                            cursor = second_element.index('Y')
                            while second_element[cursor] != ' ':
                                cursor += 1
                            first_half = second_element[:cursor]
                            second_half = f'Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]} F{final_tap_elements[tool][1]["F"]}'
                            initial_line = first_half + second_half
                        elif 'X' in second_element and 'Y' in second_element:
                            if second_element.index('Y') > second_element.index('X'):
                                cursor = second_element.index('Y')
                            else:
                                cursor = second_element.index('X')
                            while second_element[cursor] != ' ':
                                cursor += 1
                            first_half = second_element[:cursor]
                            second_half = f'Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]} F{final_tap_elements[tool][1]["F"]}'
                            initial_line = first_half + second_half
                        tapping_adjustments += initial_line + '\n'
                        current_zdepth += float(f'{final_depth / passes:0.4f}')
                        while current_zdepth >= final_depth:
                            tapping_adjustments += f'G84 Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]} F{final_tap_elements[tool][1]["F"]}\n'
                            current_zdepth += float(f'{final_depth / passes:0.4f}')
                    elif 'G80' not in second_element:
                        tapping_adjustments += f'G84 {second_element} Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]}\n'
                        current_zdepth += float(f'{final_depth / passes:0.4f}')
                        while current_zdepth >= final_depth:
                            tapping_adjustments += f'G84 Z{str(current_zdepth)} R{final_tap_elements[tool][1]["R"]} J{final_tap_elements[tool][1]["J"]}\n'
                            current_zdepth += float(f'{final_depth / passes:0.4f}')
                    elif 'G80' in second_element:
                        stop = element[0]
                        tapping_adjustments += 'G80\n'
                        tapping_adjustments += 'G94\n'
                final_tapping_output[tool] = [(f'{start:.1f}', f'{stop:.1f}'), tapping_adjustments]
            eventlog.generate('replace_text', final_tapping_output)

        eventlog.listen('confirm_choices_event', confirm_choices_event)
        eventlog.listen('show_tappingtext_event', show_tappingtext_event)
        eventlog.listen('tapping_list_generated', add_tapping_elements)


