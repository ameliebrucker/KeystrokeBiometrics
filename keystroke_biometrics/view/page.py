import ttkbootstrap as ttk
import controller.application_logic as c

class Page(ttk.Frame):
    """
    A class for representing a page
    """

    def __init__(self, root, page_name, view_change = False):        
        super().__init__(root)
        # create header
        header = ttk.Frame(self)
        header.pack(pady=20, padx=40, side= ttk.TOP, anchor="w")
        # add headline
        ttk.Label (self, text = page_name, font=root.font18).pack()
        if view_change:
            if c.template_text == "":
                # template text isn't set, navigate to template text page
                command_fixed_text = lambda: root.change_page("TemplateTextPage")
            else:
                # template text is set, navigate to recording page
                command_fixed_text = lambda: root.change_page("RecordingPage", True)
            # add navigation buttons to header
            ttk.Radiobutton(header, text="Recording Samples (free text)", width = 30, variable=root.page_from_header, command=lambda: root.change_page("RecordingPage"),value="RecordingPage", bootstyle="outline-toolbutton").grid(row=0, column=1)
            ttk.Radiobutton(header, text="Recording Samples (fixed text)", width = 30, variable=root.page_from_header, command=command_fixed_text,value="TemplateTextPage", bootstyle="outline-toolbutton").grid(row=0, column=2)
            ttk.Radiobutton(header, text="Verification", width = 30, variable=root.page_from_header, command=lambda: c.get_all_sample_identifier(root.change_page),value="VerificationPage", bootstyle="outline-toolbutton").grid(row=0, column=3)
