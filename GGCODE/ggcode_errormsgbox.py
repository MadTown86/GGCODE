import tkinter as tk
import traceback
import sys

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
        self.stacktrace = tk.Text(self, bg='black', fg='white')
        self.stacktrace.grid(column=0, row=1, sticky='nsew')
        self.stacktrace.grid_columnconfigure(0, weight=1)
        self.stacktrace.grid_rowconfigure(0, weight=1)
        self.stacktrace.insert('1.0', 'Stack Trace')
        self.stacktrace.config(state='disabled')
        self.bind('<Configure>', self.resize)
        self.mainloop()

    def resize(self, event):
        self.msg.config(width=self.winfo_width())
        self.stacktrace.config(width=self.winfo_width())

    def setMsg(self, msg):
        self.msg.config(text=msg)

    def setStackTrace(self, stacktrace):
        self.stacktrace.config(state='normal')
        self.stacktrace.delete('1.0', 'end')
        self.stacktrace.insert('1.0', traceback.format_exception(type(stacktrace), stacktrace, stacktrace.__traceback__))
        self.stacktrace.config(state='disabled')



