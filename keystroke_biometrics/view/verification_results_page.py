import ttkbootstrap as ttk
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
        mainframe = ttk.Frame(self)
        if verification_results is None:
            # samples were not comparable
            mainframe.pack(pady=(15, 0))
            ttk.Label(mainframe, text="No comparable data", font=root.font14bold).pack(anchor = ttk.W)
            ttk.Label(mainframe, text="Select samples that match in some characters or choose verification with encryption.").pack(anchor = ttk.W)
        else:
            mainframe.pack()
            results_as_text, x_thresholds, y_acceptance, y_rejection = verification_results
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
            figure.tight_layout()
            FigureCanvasTkAgg(figure, mainframe).get_tk_widget().pack(side=ttk.LEFT)
            # add text box for displaying results
            result_text_box = ScrolledText(mainframe, width=30, wrap=ttk.WORD)
            result_text_box.insert(ttk.INSERT, results_as_text)
            result_text_box.configure(state=ttk.DISABLED)
            result_text_box.pack(side=ttk.RIGHT, expand=True, fill=ttk.Y)         
        # add back button
        ttk.Button(self, text='Back to sample selection', command=lambda: c.get_all_sample_identifier(root.change_page), style="SubmitButton.TButton").pack(pady=(15, 0))
