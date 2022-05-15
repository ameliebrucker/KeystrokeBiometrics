import tkinter as tk
from view.page import Page
import cont.controller as c

class RecordingPage(Page):
    def __init__(self, root, input_data = None):
        super().__init__(root, "Recording Samples", True)

        # username frame
        username_frame = tk.Frame(self)
        username_frame.pack()
        tk.Label(username_frame, text="Username: ").grid(row=0)
        self.username = tk.StringVar(value=c.current_username)
        self.username_entry = tk.Entry(username_frame, text=self.username)
        self.username_entry.bind("<Key>", self.limit_username_length)
        self.username_entry.grid(row=0, column=1)

        #entry field for keystroke recognition
        self.focus_in_textbox = False
        self.input_textbox = tk.Text(self, height=12, width=80)
        #text_box.bind("<KeyPress>", c.validate_keyboard_entries)
        self.input_textbox.bind("<KeyPress>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), self.input_validation_failed))
        self.input_textbox.bind("<KeyRelease>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), self.input_validation_failed))
        self.input_textbox.bind("<FocusIn>", lambda e: self.focus_textbox(True))
        self.input_textbox.bind("<FocusOut>", lambda e: self.focus_textbox(False))
        self.input_textbox.bind("<Button>", lambda e: self.disable_clicks())
        #text_box.bind("<KeyRelease>",c.form_sample_from_entry)
        # zeichenkette bis zu return taste
        self.input_textbox.bind("<Return>", lambda e: c.form_sample_from_entry(self.input_textbox.get(1.0, "end-1c"), self.username.get(), root.change_page))
        # text_box = Entry(self)
        self.input_textbox.pack()

        #required text
        if c.text_for_comparison is not None:
            self.required_text_tip = tk.Label (self, text="Required text input: \"" + c.text_for_comparison + "\"")
            self.required_text_tip.pack()

        #tooltip
        self.tooltip = tk.Label (self, text = "Please type your sample text as fluent as possible in the box above. Avoid deleting characters or changing the cursor position. Finish your entry by pressing the enter key.")
        self.tooltip.pack()
    
    def focus_textbox(self, focus):
        self.focus_in_textbox = focus

    def disable_clicks(self):
        if self.focus_in_textbox:
            print("hi")
            self.input_textbox.mark_set(tk.INSERT, tk.END)
            return("break")
    
    def limit_username_length(self, event):
        #limit to 30 characters to avoid problems with long input
        if len(self.username_entry.get()) > 29:
            self.username_entry.delete(29, tk.END)

    def input_validation_failed(self, comparison_failed):
        self.input_textbox.delete("1.0","end")
        if comparison_failed:
            self.required_text_tip.config(bg= "red")
        else:
            self.tooltip.config(bg="red")
        