import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from view.page import Page
import controller.application_logic as c

class VerificationResultsPage(Page):
    """
    A class for representing the verification results page of the user interface
    """

    def __init__(self, root, verification_results = None):
        super().__init__(root, "Verification Results")
        if verification_results is None:
            # samples were not comparable
            tk.Label(self, text="The selected samples do not contain comparable data. Choose samples that match in some characters.").pack()
        else:
            results_as_text, x_thresholds, y_acceptance, y_rejection = verification_results
            # add textfield for displaying results
            result_text_box = ScrolledText(self, height=30, width=105)
            result_text_box.configure(state ='disabled')
            result_text_box.pack()
            # add diagrams
            figure = Figure(figsize=(6.2, 4.6))
            y_ticks = range(0, 101, 10)
            # add chart for acceptance rate
            p1 = figure.add_subplot(211)
            p1.plot(x_thresholds, y_acceptance, color='green')
            p1.set_xlabel('Threshold')
            p1.set_yticks(y_ticks)
            p1.set_xticks(x_thresholds)
            p1.title.set_text("Acceptance rate in %")
            # add chart for rejection rate
            p2 = figure.add_subplot(212)
            p2.plot(x_thresholds, y_rejection, color='red')
            p2.set_xlabel('Threshold')
            p2.set_yticks(y_ticks)
            p2.set_xticks(x_thresholds)
            p2.title.set_text("Rejection rate in %")
            # add diagrams to result text box
            figure.tight_layout()
            result_text_box.window_create(tk.END, window=FigureCanvasTkAgg(figure, result_text_box).get_tk_widget())
            result_text_box.window_create(tk.END, window=tk.Label(result_text_box, text=results_as_text))            
        # add back button
        tk.Button(self, text='Back to sample selection', command=lambda: c.get_all_sample_identifier(root.change_page)).pack()
