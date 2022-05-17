import tkinter as tk
import controller.application_logic as c

class Page(tk.Frame):
    """
    A class for representing a page
    """

    def __init__(self, root, page_name, view_change=False):        
        super().__init__(root)
        # create header
        header = tk.Frame(self)
        header.pack(pady=20, padx=20, side= tk.TOP, anchor="w")
        # add headline to header
        tk.Label (self, text = page_name, font=('Helvetica', 18, "bold")).pack()
        if view_change:
            # add navigation buttons to header
            tk.Radiobutton(header, text="Recording Samples", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=lambda: root.change_page(0),value=0).grid(row=0, column=1)
            tk.Radiobutton(header, text="Verification", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=lambda: c.get_all_sample_identifier(root.change_page),value=1).grid(row=0, column=2)
