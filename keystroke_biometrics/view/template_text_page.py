import tkinter as tk
from view.page import Page
import controller.application_logic as c

class TemplateTextPage(Page):
    """
    A class for representing the template text page of the user interface

    Attributes (Object)

    Methods
    """

    def __init__(self, root):
        super().__init__(root, "Set Template Text", True)
        # add textbox for keystroke recognition
        self.input_textbox = tk.Text(self, height=12, width=80)
        if c.text_for_comparison is not None:
            # add tip on required text
            self.required_text_tip = tk.Label (self, text=f"Required text input: \"{c.text_for_comparison}\"")
            self.required_text_tip.pack()
        # add tooltip on how to type properly
        self.tooltip = tk.Label (self, text = "Please type your sample text as fluent as possible in the box above. Avoid deleting characters or changing the cursor position. Finish your entry by pressing the enter key.")
        self.tooltip.pack()