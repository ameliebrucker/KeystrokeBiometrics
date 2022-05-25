import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import controller.application_logic as c

class VerificationPage(Page):
    """
    A class for representing the verification page of the user interface

    Attributes (Object)
    checked_identifiers: dictionary with identifiers as key and boolean whether they are selected as values
    encryption_check: boolean, indicates whether learnsamples should be treated as encrypted
    tooltip: label with tip for selection

    Methods
    starting_verification(callback): summarizes selected samples and starts verification process
    """

    def __init__(self, root, identifier):
        super().__init__(root, "Verification", True)
        # create dict from identifier with default selection False
        self.checked_identifiers = {identifier[i]: (tk.BooleanVar(value=False), tk.BooleanVar(value=False)) for i in range(0, len(identifier), 1)}
        # add overview for samples
        sample_selection = tk.Frame(self)
        sample_selection.pack()
        tk.Label(sample_selection, text="Learnsamples for verification process").grid(row=0, column=0)
        tk.Label(sample_selection, text="Testsamples for verification process").grid(row=0, column=1)
        learnsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=18, width=50)
        learnsamples_overview.configure(state = tk.DISABLED)
        testsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=18, width=50)
        testsamples_overview.configure(state = tk.DISABLED)
        learnsamples_overview.grid(row=1, column=0)
        testsamples_overview.grid(row=1, column=1)
        # add checkbox lists with identifiers
        for k, v in self.checked_identifiers.items():
            learnsamples_overview.window_create(tk.END, window=tk.Checkbutton(learnsamples_overview, text=k, variable=v[0], onvalue=True, offvalue=False, width=50, anchor="w", bg="white"))
            testsamples_overview.window_create(tk.END, window=tk.Checkbutton(testsamples_overview, text=k, variable=v[1], onvalue=True, offvalue=False, width=50, anchor="w", bg="white"))       
        # add encryption check
        self.encryption_check = tk.BooleanVar(value=False)
        checkbox_encryption = tk.Checkbutton(self, text="Verification process should be done with encrypted testsamples", variable=self.encryption_check, onvalue=True, offvalue=False)
        checkbox_encryption.pack()
        # add button for starting verification
        tk.Button(self, text='Start verification process', command= lambda: self.starting_verification(root.change_page)).pack()
        # add tooltip for selection
        self.tooltip = tk.Label (self, text = "Please select at least one item from each group.")
        self.tooltip.pack()

    def starting_verification(self, callback):
        """
        summarizes selected samples and starts verification process

        Parameter:
        callback: callback passed to verification function
        """

        selected_learnsamples = []
        selected_testsamples = []
        for k, v in self.checked_identifiers.items():
            if v[0].get():
                # box is checked: selected as learnsample
                selected_learnsamples.append(k)
            if v[1].get():
                # box is checked: selected as testsample
                selected_testsamples.append(k)
        if not selected_learnsamples or not selected_testsamples:
            # nothing selected, show warning
            self.tooltip.config(bg="red")
        else:
            c.verify(selected_learnsamples, selected_testsamples, self.encryption_check.get(), callback)