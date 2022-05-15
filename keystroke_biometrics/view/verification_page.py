import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import controller.application_logic as c

class VerificationPage(Page):
    """
    A class for representing the verification page of the user interface
    """

    def __init__(self, root, input_data_identifier):
        super().__init__(root, "Verification", True)
        self.input_data_identifier = input_data_identifier
        self.learnsamples_identifiers = []
        self.testsamples_identifiers = []

        #elements in view
        sample_selection = tk.Frame(self)
        sample_selection.pack()
        tk.Label(sample_selection, text="Learnsamples for verification process").grid(row=0, column=0)
        tk.Label(sample_selection, text="Testsamples for verification process").grid(row=0, column=1)
        self.learnsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=12, width=30)
        self.testsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=12, width=30)
        self.learnsamples_overview.grid(row=1, column=0)
        self.testsamples_overview.grid(row=1, column=1)

        self.fill_with_input_data()

        self.encryption_check = tk.BooleanVar(value=False)
        checkbox_encryption = tk.Checkbutton(self, text="Verification process should be done with encrypted testsamples", variable=self.encryption_check, onvalue=True, offvalue=False)
        checkbox_encryption.pack()
        # unübersichtlich, entweder in EINE datei unten, die nach ermittlung der werte c.verify aufruft und selbst failure verarbeitet oder in mehrere zeilen
        tk.Button(self, text='Start verification process', command= lambda: self.starting_verification(root.change_page)).pack()
        self.tooltip = tk.Label (self, text = "Please select at least one item from each group.")
        self.tooltip.pack()
            
    def fill_with_input_data(self):
        index = 0
        for sample in self.input_data_identifier:
            # new entry in list with default value "" (unchecked)
            self.learnsamples_identifiers.append(tk.StringVar(value=""))
            self.testsamples_identifiers.append(tk.StringVar(value=""))
            #TODO put windows untereinander
            self.learnsamples_overview.window_create(tk.END, window=tk.Checkbutton(self.learnsamples_overview, text=sample, variable=self.learnsamples_identifiers[index], onvalue=sample, offvalue=""))
            self.testsamples_overview.window_create(tk.END, window=tk.Checkbutton(self.testsamples_overview, text=sample, variable=self.testsamples_identifiers[index], onvalue=sample, offvalue=""))
            # , variable=output_data_testsamples[index], onvalue=sample, offvalue=""
            index += 1

    def starting_verification(self, callback):
        output_learnsamples = []
        output_testsamples = []
        for l in self.learnsamples_identifiers:
            if l.get() != "":
                output_learnsamples.append(l.get())
        for t in self.testsamples_identifiers:
             if t.get() != "":
                output_testsamples.append(t.get())
        if not output_learnsamples or not output_testsamples:
            self.tooltip.config(bg="red")
        else:
            c.verify(output_learnsamples, output_testsamples, self.encryption_check.get(), callback)

    """
    def get_selected_learnidentifier(self):
        output_data_learnsamples = []
        for l in self.learnsamples_identifier:
            if l.get() != "":
                output_data_learnsamples.append(l.get())
        return output_data_learnsamples

    def get_selected_testidentifier(self):
        output_data_testsamples = []
        for t in self.testsamples_identifier:
             if t.get() != "":
                output_data_testsamples.append(t.get())
        return output_data_testsamples

    def missing_selection(self):
        self.tooltip.config(bg="red")

    """     