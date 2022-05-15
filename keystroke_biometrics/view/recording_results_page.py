import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import cont.controller as c

class RecordingResultsPage(Page):
    def __init__(self, root, input_data_content_and_values = None):
        super().__init__(root, "Recording Results")
        results = input_data_content_and_values
        state_save_button = tk.NORMAL
        if results is None:
            results = "No values recorded."
            state_save_button = tk.DISABLED

        # textfield for displaying entered text
        result_text_box = ScrolledText(self, height=12, width=80)
        result_text_box.insert(tk.INSERT, results)
        result_text_box.configure(state = tk.DISABLED)
        result_text_box.pack()

        # checkbox keep entry as reference for next entrys
        reference_entry_check = tk.BooleanVar(value=False)
        if c.text_for_comparison is not None and state_save_button is not tk.DISABLED:
            reference_entry_check.set(True)
        checkbox_reference_entry = tk.Checkbutton(self, text="Keep this text as validation reference for next entry", state=state_save_button, variable=reference_entry_check, onvalue=True, offvalue=False)
        checkbox_reference_entry.pack()

        # button group
        button_group = tk.Frame(self)
        button_group.pack()
        tk.Button(button_group, text='Delete this record', command=lambda: c.delete_current_sample(reference_entry_check.get(), root.change_page)).grid(row=0, column=0)
        tk.Button(button_group, text='Save this record', state=state_save_button, command=lambda: c.archive_current_sample(reference_entry_check.get(), root.change_page)).grid(row=0, column=1)
