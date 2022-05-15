import tkinter as tk
import cont.controller as c

class Page(tk.Frame):
    def __init__(self, root, page_name, view_change=False):
       super().__init__(root)
       header = tk.Frame(self)
       header.pack(pady=20, padx=20, side= tk.TOP, anchor="w")
       tk.Label (self, text = page_name, font=('Helvetica', 18, "bold")).pack()
       if view_change:
           tk.Radiobutton(header, text="Recording Samples", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=root.change_page,value=0).grid(row=0, column=1)
           tk.Radiobutton(header, text="Verification", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=lambda: c.get_all_sample_identifier(root.change_page),value=1).grid(row=0, column=2)
