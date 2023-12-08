import tkinter as tk
from tkinter import Scrollbar
from tkinter import Canvas
from tkinter.ttk import Radiobutton

import GGCODE.ggcode_eventhandler as ggcode_eventhandler

class TappingTab(tk.Frame):
    """
    This class will create a tab that allows the user to select a tapping tool and then select options for
    rigid tapping.

    The methods in this class are as follows:
    show_tappingtext_event - This method will show the user the current tapping options that have been selected.
    confirm_choices_event - This method will confirm the user's choices for rigid tapping.
    add_tapping_elements - This method will add the tapping elements to a dictionary.
    adjust_tapping_code - This method will adjust the tapping code based on the user's choices.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        framecolor = '#CE663E'
        true_falsevar = tk.StringVar()
        self.depthvar = tk.StringVar()
        toolvar = tk.StringVar()
        self.generated_radiobuttons = {}
        self.final_tap_elements = {}
        self.initialize = False
        self.generated_lbls = {}
        self.canvas_count = 0
        count = 0

        self.toplabel = tk.Label(self, text='Choose Tap', justify='center')
        self.toplabel.grid(column=0, columnspan=2, row=count, sticky='ew')
        count += 1

        # Canvas Scrollbar
        yscrollbar_canvas = Scrollbar(self, orient='vertical')

        # Canvas Creation and Child Frame Creation
        self.scrollable_frame = Canvas(self, bg='white', width=400, height=200, scrollregion=(0, 0, 1000, 1000),
                                       yscrollcommand=yscrollbar_canvas.set)
        self.canvas_frame = tk.Frame(self.scrollable_frame, bg='white', width=1000, height=1000)
        self.scrollable_frame.create_window((0, 0), window=self.canvas_frame, anchor='nw')
        self.canvas_frame.propagate(False)
        self.scrollable_frame.grid_propagate(False)
        self.scrollable_frame.propagate(False)
        yscrollbar_canvas.config(command=self.scrollable_frame.yview)
        self.scrollable_frame.grid(column=0, row=count, sticky='ew')
        yscrollbar_canvas.grid(column=1, row=count, sticky='ns')

        # Format {'T#': ['True/False', 'Depth Increment Chosen']}
        rigid_tappingdict = {}

        # Format {'T#-----Tool Comment': [(line number, 'line of tapping code'), (line number, 'line of tapping code')]}
        self.tapping_lines = {}

        # Format {'T#': [('start line', 'stop line'), 'text string with lines of tapping code']}
        final_tapping_output = {}

        eventlog = ggcode_eventhandler.EventHandler()

        # Format {'T#': ['Tool Comment', {'Z': final z depth, 'R': retract, 'J': feedrate, 'F': feedrate},
        # (line number, drill point)]}
        self.final_tap_elements = {}

        self.grid(column=0, row=0, sticky='nsew')

        def add_options():
            """
            This method generates the options for the tapping tab and is not dynamic
            :return:
            """
            nonlocal count
            self.tap_lbl = tk.Label(self, text="Choose Repeat Rigid Tapping Options", justify='center')
            self.taptrue_radio = Radiobutton(self, text='True', value='True', variable=true_falsevar)
            self.tapfalse_radio = Radiobutton(self, text='False', value='False',
                                              variable=true_falsevar)
            self.tapdepth_lbl = tk.Label(self, text='Choose Depth Increment', justify='center')
            self.tapthird_radio = Radiobutton(self, name='third', text='Tap 1/3 Depth Increments', value='.33',
                                              variable=self.depthvar)
            self.tapfourth_radio = Radiobutton(self, name='fourth', text='Tap 1/4 Depth Increments', value='.25',
                                               variable=self.depthvar)
            self.taphalf_radio = Radiobutton(self, name='half', text='Tap 1/2 Depth Increments', value='.5',
                                             variable=self.depthvar)
            self.tapfull_radio = Radiobutton(self, name='full', text='Tap Full Depth',
                                             value='1.0', variable=self.depthvar)

            count += 1
            self.tab_spacer = tk.Label(self, text='', background=framecolor, justify='center', pady=5)
            self.tab_spacer.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.tap_lbl = tk.Label(self, text="Choose Repeat Rigid Tapping Options", justify='center')
            self.tap_lbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            tk.Radiobutton(self, text='True', value='True',
                           variable=true_falsevar, state='normal').grid(column=0, row=count, sticky='w')

            tk.Radiobutton(self, text='False', value='False',
                           variable=true_falsevar, state='normal').grid(column=1, row=count, sticky='e')
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

            self.confirm_choices = tk.Button(self, text='Store Changes', justify='center', pady=10)
            self.confirm_choices.grid(column=0, columnspan=2, row=count, sticky='ew')

            # Binding the confirm_choices button to the confirm_choices_event method
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

            self.updatetextlbl = tk.Label(self, background=framecolor, justify='center')
            self.updatetextlbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.afterupdatelbl = tk.Label(self, background=framecolor, justify='center')
            self.afterupdatelbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1

            self.send_button = tk.Button(self, text='Send To File', justify='center', pady=10)
            self.send_button.grid(column=0, columnspan=2, row=count, sticky='ew')
            self.send_button.bind("<Button-1>", adjust_tapping_code)
            count += 1

        def show_tappingtext_event(payload):
            """
            This method will show the user the current tapping options that have been selected and stored in a
            dictionary, updated as confirm_choices_event is called. The dictionary rigid_tappingdict is built from
            these choices so that changes are overwritten as the user makes new choices.

            :param payload: {tool: [true/false, depth]},
            :return: None
            """
            rigid_tappingdict[payload[0]] = [payload[1], payload[2]]
            self.show_tappingtext.config(state='normal')
            self.show_tappingtext.delete('1.0', 'end')
            for key in rigid_tappingdict.keys():
                self.show_tappingtext.insert('end', f'{key}-----{rigid_tappingdict[key]}\n')
            self.show_tappingtext.config(state='disabled')

        def confirm_choices_event(event):
            """
            This method will confirm the user's choices for rigid tapping and generate a call to the show_tappingtext
            :param event: <Button-1>
            :return: None -> generates show_tappingtext_event (payload: [tool, true/false, depth increment])
            """
            toolcontents = toolvar.get()
            true_falsecontents = true_falsevar.get()
            depthcontents = self.depthvar.get()
            if 'T' in toolcontents and true_falsecontents != '' and depthcontents != '':
                eventlog.generate('show_tappingtext_event', [toolcontents, true_falsecontents, depthcontents])
            elif 'T' not in toolcontents and true_falsecontents != '':
                self.updatetextlbl.config(text='*****SELECT A TAP RADIO BUTTON FIRST*****\n'
                                               '*****THEN SELECT A TRUE/FALSE RADIO BUTTON*****')
            elif 'T' in toolcontents and true_falsecontents == '':
                self.updatetextlbl.config(text='*****SELECT A TRUE/FALSE RADIO BUTTON*****')
            elif 'T' in toolcontents and true_falsecontents != '' and depthcontents == '':
                self.updatetextlbl.config(text='*****SELECT A DEPTH RADIO BUTTON*****')
            else:
                self.updatetextlbl.config(text='*****SELECT OPTIONS FIRST*****')

        def generate_tapping_elements(payload):
            print('generate_tapping_elements')
            """
            This method parses through the tool data accumulated during the initial file parsing and organizes key
            elements into final_tapping_output. The final_tapping_output is a dictionary with the following format:
            {'T#': ['Tool Comment', {'Z': final z depth, 'R': retract, 'J': feedrate, 'F': feedrate},
            (line number, drill point), (...)]}

            Core algorithms are:
            1. Replaces original 'F' code from IPM (inches per minute) to IPR (inches per revolution) for rigid tapping.
            2. Separates out the tool comment from the tool number.
            3. Organizes key elements for the G84 tapping cycle (Z, R, J, F) into a dictionary.
            4. Outlines the drill points for each tool
            5. Populates the final_tap_elements dictionary
            :param payload: {dictbin_tapping} sent from ggcode_textwithscrollbars.py
            :return:
            """
            self.final_tap_elements = {}
            self.tapping_lines = payload

            # tap size database: Format {'tap size string': 'converted to pitch in inches to 4 decimal places'}
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
                'M2.5X.45': f'{.45*.03937:.4f}',
                'm2.5X.45': f'{.45*.03937:.4f}',
                'M3x.5'  : f'{.5*.03937:.4f}',
                'M3X.5'  : f'{.5*.03937:.4f}',
                'm3x.5'  : f'{.5*.03937:.4f}',
                'm3X.5'  : f'{.5*.03937:.4f}',
                'M3.5x.6': f'{.6*.03937:.4f}',
                'M3.5X.6': f'{.6*.03937:.4f}',
                'm3.5x.6': f'{.6*.03937:.4f}',
                'm3.5X.6': f'{.6*.03937:.4f}',
                'M4x.7'  : f'{.7*.03937:.4f}',
                'm4X.7'  : f'{.7*.03937:.4f}',
                'm4x.7'  : f'{.7*.03937:.4f}',
                'M4X.7'  : f'{.7*.03937:.4f}',
                'M5x.8'  : f'{.8*.03937:.4f}',
                'M5X.8'  : f'{.8*.03937:.4f}',
                'm5x.8'  : f'{.8*.03937:.4f}',
                'm5X.8'  : f'{.8*.03937:.4f}',
                'M6x1'   : f'{1*.03937:.4f}',
                'M6X1'   : f'{1*.03937:.4f}',
                'm6x1'   : f'{1*.03937:.4f}',
                'm6X1'   : f'{1*.03937:.4f}',
                'M7x1'   : f'{1*.03937:.4f}',
                'M7X1'   : f'{1*.03937:.4f}',
                'm7x1'   : f'{1*.03937:.4f}',
                'm7X1'   : f'{1*.03937:.4f}',
                'M8x1.25': f'{1.25*.03937:.4f}',
                'M8X1.25': f'{1.25*.03937:.4f}',
                'm8x1.25': f'{1.25*.03937:.4f}',
                'm8X1.25': f'{1.25*.03937:.4f}',
                'M10x1.5': f'{1.5*.03937:.4f}',
                'M10X1.5': f'{1.5*.03937:.4f}',
                'm10x1.5': f'{1.5*.03937:.4f}',
                'm10X1.5': f'{1.5*.03937:.4f}',
                'M12x1.75': f'{1.75*.03937:.4f}',
                'M12X1.75': f'{1.75*.03937:.4f}',
                'm12x1.75': f'{1.75*.03937:.4f}',
                'm12X1.75': f'{1.75*.03937:.4f}',
                'M14x2'  : f'{2*.03937:.4f}',
                'M14X2'  : f'{2*.03937:.4f}',
                'm14x2'  : f'{2*.03937:.4f}',
                'm14X2'  : f'{2*.03937:.4f}',
                'M16x2'  : f'{2*.03937:.4f}',
                'M16X2'  : f'{2*.03937:.4f}',
                'm16x2'  : f'{2*.03937:.4f}',
                'm16X2'  : f'{2*.03937:.4f}',
            }

            # Loop by Tool Number
            for key in payload.keys():
                keysplit = key.split('-----')
                T = keysplit[0]
                comment = keysplit[1]
                drillmacro = {'Z': [], 'R': '', 'J': '1', 'F': ''}
                drillpoints = []

                # Check 'database' for tap size referred to in comment and update the tool's drillmacro's feedrate to chipload
                for tapsize in tap_lookup.keys():
                    if tapsize in comment:
                        drillmacro['F'] = tap_lookup[tapsize]

                # Parses through all 'tapping' lines between G84 and G80 by tool
                # Generates 'final_tap_elements' dictionary
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
                        self.final_tap_elements[T] = [comment, drillmacro, drillpoints]
            # print(f'{self.final_tap_elements=}')
            if not self.initialize:
                add_tapping_elements()
            else:
                update_tapping_elements()

        def add_tapping_elements():
            print('add_tapping_elements')
            # This section is generating a radiobutton by tap found and adding it to the tapping tab
            for T in self.final_tap_elements.keys():
                radiolabel = str(T) + 'label'
                labeltext = str(T) + '-----' + self.final_tap_elements[T][0]
                self.radiolabel = tk.Label(self.canvas_frame, text=labeltext, justify='left')
                self.radiolabel.grid(column=1, row=self.canvas_count, sticky='w')
                keyradio = str(T) + '_radio'
                self.keyradio = tk.Radiobutton(self.canvas_frame, text=str(T), value=T, variable=toolvar)
                self.keyradio.grid(column=0, row=self.canvas_count, sticky='w')

                self.generated_radiobuttons[keyradio] = self.keyradio
                self.generated_lbls[radiolabel] = self.radiolabel
                self.canvas_count += 1

            # After all tool data is added to the tapping tab, the options are added
            if not self.initialize:
                add_options()
            else:
                pass
            self.initialize = True

        def update_tapping_elements():
            print('update_tapping_elements')
            # print(f'{self.final_tap_elements=}')
            for item in self.canvas_frame.grid_slaves():
                item.destroy()
            self.canvas_count = 0
            add_tapping_elements()

        def adjust_tapping_code(event):
            """
            This method loops through the choices the user made for rigid tapping elements found in rigid_tappingdict
            and generates the final string output for the tapping cycle.

            The core algorithms are:
            1. Loop through each tap with 'True' selected for rigid tapping
            2. Isolate the lines of tapping code for the current tool
            3. Determine the number of passes to make to reach the final depth
            4. Add tapping G-code by tool until final depth is reached and record start/stop line for text updating

            :param event: <Button-1>
            :return: None
            """

            #TODO Future Fix - redundancy, just send dictbin_tapping with all required information in desired format

            # Loops through the rigid_tappingdict
            for tool, values in rigid_tappingdict.items():

                #TODO - not ideal looping construct
                for key, value in self.tapping_lines.items():
                    if tool in key:
                        # line number of the first line of tapping code original file
                        start = value[0][0]
                        # line number of the last line of tapping code original file
                        stop = value[-1][0]

                tapping_adjustments = 'G95\n'

                # If user selected True for rigid tapping
                if values[0] == 'True':

                    # This loop selects the lines of tapping code to be adjusted from tapping_lines
                    for tool_comment, values in self.tapping_lines.items():
                        if tool in tool_comment:
                            linesToAdjust = values
                        else:
                            continue

                    # The multiplier is the number of passes to make to reach the final depth
                    multiplier = rigid_tappingdict[tool][1]
                    if multiplier == '.33':
                        passes = 3
                    elif multiplier == '.25':
                        passes = 4
                    elif multiplier == '.5':
                        passes = 2
                    elif multiplier == '1.0':
                        pass

                    # The final depth is the depth of the hole to be tapped
                    final_depth = float(self.final_tap_elements[tool][1]['Z'])

                    # Loops through each line of tapping code recorded for the current tool
                    # element format (line number, 'line of tapping code')
                    for element in linesToAdjust:

                        second_element = element[1]
                        current_zdepth = float(f'{final_depth / passes:.4f}')

                        # If the line of tapping code is the first line of tapping macro
                        if 'G84' in second_element:

                            # Sometimes the first line of tapping code does not contain a drill point location
                            if 'X' not in second_element and 'Y' not in second_element:
                                initial_line = f'G84 Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"][0]} F{self.final_tap_elements[tool][1]["F"]}'
                                tapping_adjustments += initial_line + '\n'
                                current_zdepth += float(f'{final_depth / passes:.4f}')
                                while current_zdepth >= final_depth:
                                    tapping_adjustments += f'G84 Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"][0]} F{self.final_tap_elements[tool][1]["F"]}\n'
                                    current_zdepth += float(f'{final_depth / passes:.4f}')
                                continue
                            # If first line of tapping macro contains a drill point location
                            # Locations can be relative to the current position and you need to check
                            # for X and/or Y in the line of code and update accordingly
                            # In addition, some machine controls can have Y or X first in this line of code
                            # Necessary to check which location is greater and slice information from there
                            elif 'X' in second_element and 'Y' not in second_element:
                                cursor = element.index('X')
                                while second_element[cursor] != ' ':
                                    cursor += 1
                                first_half = second_element[:cursor]
                                second_half = f'Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]} F{self.final_tap_elements[tool][1]["F"]}'
                                initial_line = first_half + second_half
                            elif 'X' not in second_element and 'Y' in second_element:
                                cursor = second_element.index('Y')
                                while second_element[cursor] != ' ':
                                    cursor += 1
                                first_half = second_element[:cursor]
                                second_half = f'Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]} F{self.final_tap_elements[tool][1]["F"]}'
                                initial_line = first_half + second_half
                            elif 'X' in second_element and 'Y' in second_element:
                                if second_element.index('Y') > second_element.index('X'):
                                    cursor = second_element.index('Y')
                                else:
                                    cursor = second_element.index('X')
                                while second_element[cursor] != ' ':
                                    cursor += 1
                                first_half = second_element[:cursor]
                                second_half = f'Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]} F{self.final_tap_elements[tool][1]["F"]}'
                                initial_line = first_half + second_half
                            tapping_adjustments += initial_line + '\n'
                            current_zdepth += float(f'{final_depth / passes:0.4f}')
                            while current_zdepth >= final_depth:
                                tapping_adjustments += f'G84 Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]} F{self.final_tap_elements[tool][1]["F"]}\n'
                                current_zdepth += float(f'{final_depth / passes:0.4f}')
                        # If the line of tapping code is not the first line of tapping macro
                        elif 'G80' not in second_element:
                            tapping_adjustments += f'G84 {second_element} Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]}\n'
                            current_zdepth += float(f'{final_depth / passes:0.4f}')
                            while current_zdepth >= final_depth:
                                tapping_adjustments += f'G84 Z{str(current_zdepth)} R{self.final_tap_elements[tool][1]["R"]} J{self.final_tap_elements[tool][1]["J"]}\n'
                                current_zdepth += float(f'{final_depth / passes:0.4f}')
                        # If the line of tapping code is the last line of tapping macro
                        elif 'G80' in second_element:
                            stop = element[0]
                            tapping_adjustments += 'G80\n'
                            tapping_adjustments += 'G94\n'
                    # final_tapping_output is a dictionary with the following format:
                    # {'T#': [('start line', 'stop line'), 'tapping adjustments']}
                    final_tapping_output[tool] = [(f'{start:.1f}', f'{stop:.1f}'), tapping_adjustments]
                    # print(f'{final_tapping_output=}')

            # replace_tapping_text is listened to by GGCODE_TextWithScrollbars.py
            eventlog.generate('replace_tapping_text', final_tapping_output)

        # Generated internally to this class
        eventlog.listen('confirm_choices_event', confirm_choices_event)

        # Generated internally to this class
        eventlog.listen('show_tappingtext_event', show_tappingtext_event)

        # This event is generated by ggcode_textwithscrollbars.py
        eventlog.listen('tapping_list_generated', generate_tapping_elements)

        eventlog.listen('update_tapping_elements', update_tapping_elements)


