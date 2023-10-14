import tkinter as tk
from tkinter.ttk import Notebook

class TextWithScrollBars(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = tk.Scrollbar(self, orient="horizontal")
        yscrollbar = tk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(
            self,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set
        )

        xscrollbar.config(command=self.text.xview)
        yscrollbar.config(command=self.text.yview)

        self.text.grid(row=0, column=0, rowspan=2, sticky="NWES")
        yscrollbar.grid(row=0, column=1, rowspan=2, sticky="NS")
        xscrollbar.grid(row=1, column=0, sticky="EW")
# Root Elements
root = tk.Tk()
root.grid_columnconfigure(0, weight=1)
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
tabs = Notebook(right_pane)

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

tabs.add(child=file_tab, text="FILE", state="normal")
tabs.grid(column=0, row=0, sticky='nsew')






if __name__ == "__main__":
    root.mainloop()