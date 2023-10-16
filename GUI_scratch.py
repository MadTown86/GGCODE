import tkinter as tk
from tkinter.ttk import Notebook

# Root Elements
root = tk.Tk()
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.geometry('1000x1000')
root.configure(bg='gray', relief='flat')

# Notebook Creation


# View Pane Elements
left_pane = tk.Frame(master=root, bg='#597275', relief='raised', height=1000, width=10)
left_pane.propagate(True)
left_pane.grid(column=0, row=0, sticky='nsew')
left_pane.grid_columnconfigure(0, weight=1)
left_pane.grid_rowconfigure(0, weight=1)

xscrollbar = tk.Scrollbar(orient='horizontal')
yscrollbar = tk.Scrollbar(orient='vertical')

textbox = tk.Text(master=left_pane, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
textbox.grid(column=0, row=0, sticky='nsew')
textbox.grid_rowconfigure(0, weight=1)
textbox.grid_columnconfigure(0, weight=1)
yscrollbar.grid(row=0, column=1, sticky='ns')
xscrollbar.grid(row=1, column=0, sticky='ew')

# Tab Pane Elements
right_pane = tk.Frame(master=root, bg="#9E6A81", border=1, borderwidth=5, padx=5, pady=5, relief='raised', height=1000, width=400)
right_pane.grid(column=2, row=0, sticky='nsew')
right_pane.grid_rowconfigure(0, weight=1)
confirm_btn = tk.Button(master=root, text='Confirm')
confirm_btn.grid(column=2, row=1)
right_pane.grid_propagate(False)
tabs = Notebook(right_pane)

# File Tab Elements
file_tab = tk.Frame(master=tabs, bg='#9C5935', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
browse_lbl = tk.Label(master=file_tab, text='Please Choose An *.NC File Or Equivalent', justify='left')
browse_btn = tk.Button(master=file_tab, text='Browse', justify='left')
show_contentslbl = tk.Label(master=file_tab, text='Click To Show File Contents', justify='left')
contents_btn = tk.Button(master=file_tab, text='Show Contents', justify='left')

browse_lbl.grid(column=0, row=0, sticky='ew')
browse_btn.grid(column=0, row=1)
show_contentslbl.grid(column=0, row=2, sticky='ew')
contents_btn.grid(column=0, row=3)
file_tab.grid_rowconfigure('1 2 3 4', uniform='1')
file_tab.grid(column=0, row=0, sticky='nsew')

# Renumber Tab Elements
renumber_tab = tk.Frame(master=tabs, bg='#C27027', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
v = tk.StringVar(master=renumber_tab, value='1')
ren_lbl_1 = tk.Label(master=renumber_tab, text="Please Choose One Renumber Option", justify='center')
no_radio = tk.Radiobutton(master=renumber_tab, text='No Changes', value='1', variable=v)
remove_radio = tk.Radiobutton(master=renumber_tab, text='Remove N Numbers', value='2', variable=v)
renumber_radio = tk.Radiobutton(master=renumber_tab, text='Renumber All Lines', value='3', variable=v)
onlytools_radio = tk.Radiobutton(master=renumber_tab, text='Only Tool Changes', value='4', variable=v)
ren_lbl_2 = tk.Label(master=renumber_tab, text='Enter Increment Value', justify='center')
ren_lbl_3 = tk.Label(master=renumber_tab, text='Enter Max N-Number', justify='center')
ren_lbl_4 = tk.Label(master=renumber_tab, text='Enter Starting N-Number', justify='center')
increment_entry = tk.Entry(master=renumber_tab, width=3, bg='white', justify='left')
maxn_entry = tk.Entry(master=renumber_tab, width=6, bg='white', justify='left')
start_entry = tk.Entry(master=renumber_tab, width=6, bg='white', justify='left')

renumber_tab.grid_rowconfigure('0 1 2 3 4 5 6 7 8 9 10', uniform='1')
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
renumber_tab.grid(column=0, row=0, sticky='nsew')

# Tapping Tab Elements
tapping_tab = tk.Frame(master=tabs, bg='#CE663E', border=5, borderwidth=5, padx=5, pady=5, relief='flat')
intvar = tk.IntVar(master=tapping_tab, value=1)
depthvar = tk.IntVar(master=tapping_tab, value=5)
tap_lbl = tk.Label(master=tapping_tab, text="Choose Repeat Rigid Tapping Options", justify='center')
taptrue_radio = tk.Radiobutton(master=tapping_tab, text='True', value=True, variable=intvar)
tapfalse_radio = tk.Radiobutton(master=tapping_tab, text='False', value=False, variable=intvar)
tapdepth_lbl = tk.Label(master=tapping_tab, text='Choose Depth Increment', justify='center')
tapthird_radio = tk.Radiobutton(master=tapping_tab, text='Tap 1/3 Depth Increments', value='.33', variable=depthvar)
tapfourth_radio = tk.Radiobutton(master=tapping_tab, text='Tap 1/4 Depth Increments', value='.25', variable=depthvar)
taphalf_radio = tk.Radiobutton(master=tapping_tab, text='Tap 1/2 Depth Increments', value='.5', variable=depthvar)
tapfull_radio = tk.Radiobutton(master=tapping_tab, text='Tap Full Depth', value='1.0', variable=depthvar)

tapping_tab.grid_rowconfigure('0 1 2 3 4 5', uniform='1')
tap_lbl.grid(column=0, columnspan=2, row=0, sticky='ew')
taptrue_radio.grid(column=0, row=1, sticky='w')
tapfalse_radio.grid(column=1, row=1, sticky='e')
tapdepth_lbl.grid(column=0, columnspan=2, row=2, sticky='ew')
tapfull_radio.grid(column=0, columnspan=2, row=3, sticky='w')
taphalf_radio.grid(column=0, columnspan=2, row=4, sticky='w')
tapthird_radio.grid(column=0, columnspan=2, row=5, sticky='w')
tapfourth_radio.grid(column=0, columnspan=2, row=6, sticky='w')
tapping_tab.grid(column=0, row=0, sticky='nsew')


# Tab Entry Into Notebook
tabs.add(child=file_tab, text="FILE", state="normal")
tabs.add(child=renumber_tab, text='RENUMBER', state="normal")
tabs.add(child=tapping_tab, text='TAPPING', state='normal')
tabs.grid(column=0, row=0, sticky='nsew')

if __name__ == "__main__":
    root.mainloop()