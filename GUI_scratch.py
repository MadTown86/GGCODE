import tkinter as tk

root = tk.Tk()

mainframe = tk.Frame(
    master=root,
    height=400,
    width=800
)

mainframe.grid(
    column=0,
    columnspan=2,
    row=0,
    rowspan=2
)

leftframe = tk.Frame(
    master=mainframe,
    background='red'
)

leftframe.grid(
    row=0,
    column=0,
    rowspan=2
)

rightframe = tk.Frame(
    master=mainframe,
    background='blue'
)



l1 = tk.Label(
    text="Label1"
)

l2 = tk.Label(
    text="Label2"
)

l3 = tk.Label(
    text="Label3"
)

l4 = tk.Label(
    text="Label4"
)

l1.grid(
    column=0,
    row=0,
)

l2.grid(
    column=1,
    row=0,
)

l3.grid(
    column=0,
    row=1,
)

l4.grid(
    column=1,
    row=1,
)

if __name__ == "__main__":
    root.mainloop()


