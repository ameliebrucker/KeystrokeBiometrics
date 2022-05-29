import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import controller.application_logic as c

class RecordingResultsPage(Page):
    """
    A class for representing the recording results page of the user interface
    """

    def __init__(self, root, fixed_text_and_results):
        super().__init__(root, "Recording results")
        fixed_text, results = fixed_text_and_results
        state_save_button = ttk.NORMAL
        if results is None:
            results = "No values recorded.\n\nThe input was empty, shorter than the template text or no time values could be evaluated."
            # disable save button and checkbox for reference entry
            state_save_button = ttk.DISABLED
        # add textfield for displaying entered content and recorded value
        result_text_box = ScrolledText(self, height=20, width=100, wrap=ttk.WORD)
        result_text_box.insert(ttk.INSERT, results)
        result_text_box.configure(state = ttk.DISABLED)
        result_text_box.pack(pady=(15, 0))
        # add button group for save / delete
        button_group = ttk.Frame(self)
        button_group.pack(pady=(15, 0))
        ttk.Button(button_group, text='Delete this sample', command=lambda: c.delete_current_sample(fixed_text, root.change_page), bootstyle=ttk.PRIMARY, style="SubmitButton.TButton").grid(row=0, column=0, padx=2)
        ttk.Button(button_group, text='Save this sample', state=state_save_button, command=lambda: c.archive_current_sample(fixed_text, root.change_page), bootstyle=ttk.PRIMARY, style="SubmitButton.TButton").grid(row=0, column=1, padx=2)
