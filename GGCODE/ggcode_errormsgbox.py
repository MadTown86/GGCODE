import tkinter as tk

class GGCODE_ErrorMsgBox(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('GGCODE Error')
        self.geometry('500x500')
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.msg = tk.Label(self, text='Error', justify='left')
        self.msg.grid(column=0, row=0, sticky='nsew')
        self.close_btn = tk.Button(self, text='Close', command=self.destroy)
        self.close_btn.grid(column=0, row=1, sticky='s')

    def start(self):
        self.mainloop()

    def setMsg(self, msg):
        self.msg.config(text=msg)




