import tkinter as tk
from unicodedata import decimal

import MRP_EventHandler
class TappingTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        intvar = tk.IntVar(self, value=1)
        depthvar = tk.IntVar(self, value=5)
        eventlog = MRP_EventHandler.EventHandler()
        count = 0

        final_tap_elements = {}

        self.grid(column=0, row=0, sticky='nsew')
        def add_options():
            nonlocal count
            tap_lbl = tk.Label(self, text="Choose Repeat Rigid Tapping Options", justify='center')
            taptrue_radio = tk.Radiobutton(self, text='True', value=True, variable=intvar)
            tapfalse_radio = tk.Radiobutton(self, text='False', value=False, variable=intvar)
            tapdepth_lbl = tk.Label(self, text='Choose Depth Increment', justify='center')
            tapthird_radio = tk.Radiobutton(self, text='Tap 1/3 Depth Increments', value='.33',
                                            variable=depthvar)
            tapfourth_radio = tk.Radiobutton(self, text='Tap 1/4 Depth Increments', value='.25',
                                             variable=depthvar)
            taphalf_radio = tk.Radiobutton(self, text='Tap 1/2 Depth Increments', value='.5',
                                           variable=depthvar)
            tapfull_radio = tk.Radiobutton(self, text='Tap Full Depth', value='1.0', variable=depthvar)

            count += 1
            tap_lbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            taptrue_radio.grid(column=0, row=count, sticky='w')
            tapfalse_radio.grid(column=1, row=count, sticky='e')
            count += 1
            tapdepth_lbl.grid(column=0, columnspan=2, row=count, sticky='ew')
            count += 1
            tapfull_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            taphalf_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            tapthird_radio.grid(column=0, columnspan=2, row=count, sticky='w')
            count += 1
            tapfourth_radio.grid(column=0, columnspan=2, row=count, sticky='w')

        def add_tapping_elements(payload):
            nonlocal final_tap_elements
            tap_lookup = {
                '5-44'   : f'{1/44: .4f}',
                '5-40'   : f'{1/40: .4f}',
                '6-32'   : f'{1/32: .4f}',
                '8-32'   : f'{1/32: .4f}',
                '10-24'  : f'{1/24: .4f}',
                '10-32'  : f'{1/32: .4f}',
                '1/4-20' : f'{1/20: .4f}',
                '1/4-28' : f'{1/28: .4f}',
                '5/16-18': f'{1/18: .4f}',
                '5/16-24': f'{1/24: .4f}',
                '3/8-16' : f'{1/16: .4f}',
                '3/8-24' : f'{1/24: .4f}',
                '7/16-14': f'{1/14: .4f}',
                '7/16-20': f'{1/20: .4f}',
                '1/2-13' : f'{1/13: .4f}',
                '1/2-20' : f'{1/20: .4f}',
                '9/16-12': f'{1/12: .4f}',
                '9/16-18': f'{1/18: .4f}',
                '5/8-11' : f'{1/11: .4f}',
                '5/8-18' : f'{1/18: .4f}',
                '3/4-10' : f'{1/10: .4f}',
                '3/4-16' : f'{1/16: .4f}',
                '7/8-9'  : f'{1/9: .4f}',
                '7/8-14' : f'{1/14: .4f}',
                '1-8'    : f'{1/8: .4f}',
                '1-12'   : f'{1/12: .4f}',
                'M2.5x.45': f'{.45*25.4: .4f}',
                'M3x.5'  : f'{.5*25.4: .4f}',
                'M3.5x.6': f'{.6*25.4: .4f}',
                'M4x.7'  : f'{.7*25.4: .4f}',
                'M5x.8'  : f'{.8*25.4: .4f}',
                'M6x1'   : f'{1*25.4: .4f}',
                'M7x1'   : f'{1*25.4: .4f}',
                'M8x1.25': f'{1.25*25.4: .4f}',
                'M10x1.5': f'{1.5*25.4: .4f}',
                'M12x1.75': f'{1.75*25.4: .4f}',
                'M14x2'  : f'{2*25.4: .4f}',
                'M16x2'  : f'{2*25.4: .4f}',
            }
            for key in payload.keys():
                keysplit = key.split('-----')
                T = keysplit[0]
                comment = keysplit[1]
                for tapsize in tap_lookup.keys():
                    if tapsize in comment:
                        final_tap_elements[T] = (tap_lookup[tapsize], payload[key])
            print(final_tap_elements)
            nonlocal count
            self.toplabel = tk.Label(self, text='Choose Tap', justify='center')
            for T in final_tap_elements.keys():
                radiolabel = str(T) + 'label'
                labeltext = str(T) + '-----' + comment
                self.radiolabel = tk.Label(self, text=labeltext, justify='left')
                self.radiolabel.grid(column=1, row=count, sticky='w')
                keyradio = str(T) + '_radio'
                self.keyradio = tk.Radiobutton(self, text=key, value=key, variable=intvar)
                self.keyradio.grid(column=0, row=count, sticky='w')
                count += 1
            add_options()



        eventlog.listen('tapping_list_generated', add_tapping_elements)

