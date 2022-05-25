import ttkbootstrap as ttk
from view.page import Page
import controller.application_logic as c

class TemplateTextPage(Page):
    """
    A class for representing the template text page of the user interface

    Attributes (Object)

    Methods
    """

    def __init__(self, root):
        super().__init__(root, "Recording (fixed text)", True)
        mainframe = ttk.Frame(self)
        mainframe.pack(pady=(15, 0))
        # add instructions
        ttk.Label(mainframe, text="Enter your template text", font=root.font14bold).pack(anchor = ttk.W)
        ttk.Label(mainframe, text="You can also paste a copied text. For the template text no keystrokes will be recorded.").pack(anchor = ttk.W)
        # add textbox for sample text
        template_textbox = ttk.Text(mainframe, height=12, width=100)
        template_textbox.insert(ttk.INSERT, c.template_text)
        template_textbox.focus_set()
        template_textbox.pack()
        # add button for saving
        ttk.Button(mainframe, text="Set template text", command=lambda:c.set_template_text(template_textbox.get(1.0, ttk.END), root.change_page), bootstyle=ttk.PRIMARY).pack()