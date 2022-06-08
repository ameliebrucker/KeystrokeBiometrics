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
        header.pack(pady=(20, 0), padx=40, anchor=ttk.W)
        if view_change:
            # page should contain radiobuttons for changing view (navigation)
            if c.template_text == "":
                # template text isn't set, navigate to template text page
                command_fixed_text = lambda: root.change_page("TemplateTextPage")
            else:
                # template text is set, navigate to recording page
                command_fixed_text = lambda: root.change_page("RecordingPage", True)
            # add navigation buttons to header
            ttk.Radiobutton(header, text="Recording samples (free text)", variable=root.page_from_header, command=lambda: root.change_page("RecordingPage"),value="RecordingPage", bootstyle=ttk.OUTLINE + ttk.TOOLBUTTON, width = 30).grid(row=0, column=1)
            ttk.Radiobutton(header, text="Recording samples (fixed text)", variable=root.page_from_header, command=command_fixed_text,value="TemplateTextPage", bootstyle=ttk.OUTLINE + ttk.TOOLBUTTON, width = 30).grid(row=0, column=2)
            ttk.Radiobutton(header, text="Verification", variable=root.page_from_header, command=lambda: c.get_all_sample_identifiers(root.change_page),value="VerificationPage", bootstyle=ttk.OUTLINE + ttk.TOOLBUTTON, width = 30).grid(row=0, column=3)
            ttk.Separator(self).pack(expand=True, fill=ttk.X, pady=(10, 20), padx=40)
        # add headline
        ttk.Label (self, text = page_name, style="Headline.TLabel").pack()
        
