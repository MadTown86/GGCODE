import tkinter as tk
import GGCODE_EventHandler

class ToolTab(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs),
        self.grid(column=0, row=0, sticky='nsew')
        eventlog = GGCODE_EventHandler.EventHandler()


        def add_tool_entries(payload):
            count_box = 1
            count_label = 0
            for key, value in payload.items():
                keyl = str(key) + 'label'
                valuel = str(value) +'label'
                self.keyl = tk.Label(self, text=key, justify='left')
                self.keyl.grid(column=0, row=count_label, sticky='w')
                self.valuel = tk.Label(self, text=value, justify='left')
                self.valuel.grid(column=1, row=count_label, sticky='w')
                self.key = tk.Entry(self, show=key)
                self.key.grid(column=0, row=count_box, sticky='w')
                self.value = tk.Entry(self, show=value)
                self.value.grid(column=1, row=count_box, sticky='w')
                count_box += 2
                count_label += 2


        eventlog.listen('tool_list_generated', add_tool_entries)