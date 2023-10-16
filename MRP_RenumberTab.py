"""
Renumber Tab Class
"""
import tkinter as tk

class RenumberTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        v = tk.StringVar(self, value='1')
        ren_lbl_1 = tk.Label(self, text="Please Choose One Renumber Option", justify='center')
        no_radio = tk.Radiobutton(self, text='No Changes', value='1', variable=v)
        remove_radio = tk.Radiobutton(self, text='Remove N Numbers', value='2', variable=v)
        renumber_radio = tk.Radiobutton(self, text='Renumber All Lines', value='3', variable=v)
        onlytools_radio = tk.Radiobutton(self, text='Only Tool Changes', value='4', variable=v)
        ren_lbl_2 = tk.Label(self, text='Enter Increment Value', justify='center')
        ren_lbl_3 = tk.Label(self, text='Enter Max N-Number', justify='center')
        ren_lbl_4 = tk.Label(self, text='Enter Starting N-Number', justify='center')
        increment_entry = tk.Entry(self, width=3, bg='white', justify='left')
        maxn_entry = tk.Entry(master=self, width=6, bg='white', justify='left')
        start_entry = tk.Entry(master=self, width=6, bg='white', justify='left')

        self.grid_rowconfigure('0 1 2 3 4 5 6 7 8 9 10', uniform='1')
        ren_lbl_1.grid(column=0, row=0, sticky='ew')
        no_radio.grid(column=0, row=1, sticky='w')
        remove_radio.grid(column=0, row=2, sticky='w')
        renumber_radio.grid(column=0, row=3, sticky='w')
        onlytools_radio.grid(column=0, row=4, sticky='w')
        ren_lbl_2.grid(column=0, row=5, sticky='ew')
        increment_entry.grid(column=0, row=6, sticky='w')
        ren_lbl_3.grid(column=0, row=7, sticky='ew')
        maxn_entry.grid(column=0, row=8, sticky='w')
        ren_lbl_4.grid(column=0, row=9, sticky='ew')
        start_entry.grid(column=0, row=10, sticky='w')
        self.grid(column=0, row=0, sticky='nsew')