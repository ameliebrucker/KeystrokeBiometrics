import tkinter as tk
from view.page import Page
import controller.application_logic as c

class RecordingPage(Page):
    """
    A class for representing the recording page of the user interface

    Attributes (Object)
    username_entry = entry widget for username
    input_textbox = textbox in which keystrokes are recorded
    required_text_tip = label with tip on required text
    tooltip = label with tip on how to type

    Methods
    set_cursor_to_end(): sets cursor to the end of input_textbox
    limit_username_length(event): limits username to 30 characters
    input_validation_failed(comparison_failed): displays information about failing input validation
    """

    def __init__(self, root):
        super().__init__(root, "Recording Samples", True)
        # add username entry field + label
        username_frame = tk.Frame(self)
        username_frame.pack()
        tk.Label(username_frame, text="Username: ").grid(row=0)
        username = tk.StringVar(value=c.current_username)
        self.username_entry = tk.Entry(username_frame, text=username)
        self.username_entry.bind("<Key>", self.limit_username_length)
        self.username_entry.grid(row=0, column=1)
        # add textbox for keystroke recognition
        self.input_textbox = tk.Text(self, height=12, width=80)
        self.input_textbox.bind("<KeyPress>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), self.input_validation_failed))
        self.input_textbox.bind("<KeyRelease>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), self.input_validation_failed))
        # set return key as input exit
        self.input_textbox.bind("<Return>", lambda e: c.form_sample_from_entry(self.input_textbox.get(1.0, "end-1c"), username.get(), root.change_page))
        # prevent user from changing cursor position
        self.input_textbox.bind("<Button>", lambda e: self.set_cursor_to_end())
        self.input_textbox.pack()
        if c.text_for_comparison is not None:
            # set tip on required text
            self.required_text_tip = tk.Label (self, text=f"Required text input: \"{c.text_for_comparison}\"")
            self.required_text_tip.pack()
        # set tooltip on how to type properly
        self.tooltip = tk.Label (self, text = "Please type your sample text as fluent as possible in the box above. Avoid deleting characters or changing the cursor position. Finish your entry by pressing the enter key.")
        self.tooltip.pack()

    def set_cursor_to_end(self):
        """
        sets cursor to the end of input_textbox to prevent user from writing to another position
        """

        self.input_textbox.focus_set()
        self.input_textbox.mark_set(tk.INSERT, tk.END)
        # prevent default behaviour of setting cursor to clicked position
        return("break")
    
    def limit_username_length(self, event):
        """
        limits username to 30 characters

        Parameter:
        event: keystroke event which triggered function
        """

        if len(self.username_entry.get()) > 29:
            # delete last char
            self.username_entry.delete(29, tk.END)

    def input_validation_failed(self, comparison_failed):
        """
        displays information about failing input validation for user

        Parameter:
        comparison_failed: boolean, indicates whether the comparison with the required text failed
        """

        # delete corrupted content completely
        self.input_textbox.delete("1.0", tk.END)
        if comparison_failed:
            self.required_text_tip.config(bg= "red")
        else:
            self.tooltip.config(bg="red")
        