import tkinter as tk

class TappingTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        intvar = tk.IntVar(self, value=1)
        depthvar = tk.IntVar(self, value=5)
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

        self.grid_rowconfigure('0 1 2 3 4 5', uniform='1')
        tap_lbl.grid(column=0, columnspan=2, row=0, sticky='ew')
        taptrue_radio.grid(column=0, row=1, sticky='w')
        tapfalse_radio.grid(column=1, row=1, sticky='e')
        tapdepth_lbl.grid(column=0, columnspan=2, row=2, sticky='ew')
        tapfull_radio.grid(column=0, columnspan=2, row=3, sticky='w')
        taphalf_radio.grid(column=0, columnspan=2, row=4, sticky='w')
        tapthird_radio.grid(column=0, columnspan=2, row=5, sticky='w')
        tapfourth_radio.grid(column=0, columnspan=2, row=6, sticky='w')
        self.grid(column=0, row=0, sticky='nsew')