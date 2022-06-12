import ttkbootstrap as ttk
from view.page import Page
import controller.application_logic as c

class TemplateTextPage(Page):
    """
    A class for representing the template text page of the user interface
    """

    def __init__(self, root):
        super().__init__(root, "Recording (fixed text)", True)
        mainframe = ttk.Frame(self)
        mainframe.pack(pady=(15, 0))
        # add instructions
        ttk.Label(mainframe, text="Enter your template text", style="MediumHeadline.TLabel").pack(anchor = ttk.W)
        ttk.Label(mainframe, text="For the template text no keystrokes will be recorded.").pack(anchor = ttk.W)
        # add textbox for sample text
        template_textbox_border = ttk.Frame(mainframe, bootstyle=ttk.LIGHT)
        template_textbox_border.pack(fill=ttk.X)
        template_textbox = ttk.Text(template_textbox_border, height=12, width=100, wrap=ttk.WORD)
        template_textbox.insert(ttk.INSERT, c.template_text)
        template_textbox.focus_set()
        template_textbox.pack(padx=1, pady=1)
        # bind return key to setting template text
        template_textbox.bind("<Return>", lambda e: c.set_template_text(template_textbox.get(1.0, "end-1c"), root.change_page))
        # add button for setting template text
        ttk.Button(mainframe, text="Set template text", command=lambda:c.set_template_text(template_textbox.get(1.0, ttk.END), root.change_page), bootstyle=ttk.PRIMARY, style="SubmitButton.TButton").pack(pady=(6, 0))