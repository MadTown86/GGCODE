import tkinter as tk
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
            yscrollcommand=yscrollbar.set,
        )

        xscrollbar.config(command=self.text.xview)
        yscrollbar.config(command=self.text.yview)

        self.text.grid(row=0, column=0, sticky="nsew")
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar.grid(row=1, column=0, sticky="ew")

    def update_text(self, msg, header: str = "- DEFAULT -"):
        """
        This function updates file_textbox with contents of chosen file
        :param msg: contents of chosen file
        :param header:
        :return: None
        """
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", str(f'STATUS MESSAGE: {header} -> \n{msg}'))
        self.text.config(state="disabled")

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.grid_propagate(True)
#     root.grid_columnconfigure(0, weight=1)
#     root.grid_rowconfigure(0, weight=9)
#     root.grid_rowconfigure(1, weight=1)
#     T = TextWithScrollBars(master=root)
#     T.grid(column=0, row=0, sticky='nsew')
#     T.update_text('Message Text', "NOT DEFAULT ANYMORE")
#     root.mainloop()