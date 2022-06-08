import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from view.page import Page
import controller.application_logic as c

class VerificationResultsPage(Page):
    """
    A class for representing the verification results page of the user interface

    Attributes (Object)
    results_as_text: verification results as text
    y_acceptance: acceptance values for y axis of acceptance chart as list
    y_rejection: rejection values for y axis of rejection chart as list
    figure: figure with plotted charts
    line_plot1: chart line of plot 1 (acceptance) as Line2D object
    line_plot2: chart line of plot 2 (rejection) as Line2D object
    result_text_box: text box for displaying results as text
    max_threshold: maximal threshold as int
    threshold_button: button for reloading results with new maximal threshold

    Methods
    show_results(): displays results in diagram and text box
    validate_threshold(input): validates input to guarantee threshold between 0 and 9999
    update_results(): updates result based on new threshold
    """

    def __init__(self, root, verification_results = None):
        super().__init__(root, "Verification results")
        mainframe = ttk.Frame(self)
        if verification_results is None:
            # samples were not comparable
            mainframe.pack(pady=(15, 15))
            ttk.Label(mainframe, text="No comparable data", style="MediumHeadline.TLabel").pack(anchor = ttk.W)
            ttk.Label(mainframe, text="Select samples that match in some characters or choose verification with encryption.").pack(anchor = ttk.W)
        else:
            mainframe.pack()
            self.results_as_text, self.y_acceptance, self.y_rejection, max_threshold_input = verification_results 
            # add diagrams
            self.figure = Figure(figsize=(6.2, 4.6))
            # set thresholds values for x axis as number between 0 and 1
            x_thresholds = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
            y_ticks = range(0, 101, 10)
            # add chart for acceptance rate
            plot1 = self.figure.add_subplot(211)
            self.line_plot1, = plot1.plot(x_thresholds, self.y_acceptance, color='green')
            plot1.set_yticks(y_ticks)
            plot1.set_xticks(x_thresholds)
            plot1.set_xlabel('Threshold')
            plot1.title.set_text("Acceptance rate in %")
            # add chart for rejection rate
            plot2 = self.figure.add_subplot(212)
            self.line_plot2, = plot2.plot(x_thresholds, self.y_rejection, color='red')
            plot2.set_yticks(y_ticks)
            plot2.set_xticks(x_thresholds)
            plot2.set_xlabel('Threshold')
            plot2.title.set_text("Rejection rate in %")
            self.figure.tight_layout()
            FigureCanvasTkAgg(self.figure, mainframe).get_tk_widget().pack(side=ttk.LEFT)           
            # add frame for interactive elements (scrollbar + box for adjusting threshold)
            interaction_frame = ttk.Frame(mainframe)
            interaction_frame.pack(side=ttk.RIGHT, expand=True, fill=ttk.Y)
            # add text box for displaying text results
            self.result_text_box = ScrolledText(interaction_frame, width=22, wrap=ttk.WORD)
            self.result_text_box.pack(pady=(0, 4), fill=ttk.X)
            # add box for adjusting threshold
            threshold_border = ttk.Labelframe(interaction_frame, bootstyle=ttk.PRIMARY, text="Adjust the threshold")
            threshold_border.pack()
            # add threshold entry field + label
            threshold_frame = ttk.Frame(threshold_border)
            threshold_frame.pack(padx=2)
            ttk.Label(threshold_frame, text = "Maximal threshold: ").pack(side=ttk.LEFT)
            self.max_threshold = ttk.IntVar(value=max_threshold_input)
            # validate threshold as number between 0 and 9999 by registering validation function
            validate_threshold_command = (root.register(self.validate_threshold), '%P')
            threshold_entry = ttk.Entry(threshold_frame, text=self.max_threshold, validate="key", validatecommand=validate_threshold_command, width=6)
            threshold_entry.pack(side=ttk.LEFT)
            ttk.Label(threshold_frame, text="ms").pack(side=ttk.RIGHT)
            # add button to apply new threshold
            self.threshold_button = ttk.Button(threshold_border, text="Apply new threshold", command=self.update_results, style="SubmitButton.TButton")
            self.threshold_button.pack(pady=4)
            # show results as text and diagram
            self.show_results() 
        # add back button
        ttk.Button(self, text="Back to sample selection", command=lambda: c.get_all_sample_identifiers(root.change_page), style="SubmitButton.TButton").pack()

    def show_results(self):
        """
        displays results in diagram and text box
        """

        # fill diagrams with results
        self.line_plot1.set_ydata(self.y_acceptance)
        self.line_plot2.set_ydata(self.y_rejection)
        # redraw lines and hold event until it is finished
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        # fill text box with results
        self.result_text_box.configure(state=ttk.NORMAL) 
        self.result_text_box.delete("1.0", ttk.END)
        self.result_text_box.insert(ttk.END, self.results_as_text)
        self.result_text_box.configure(state=ttk.DISABLED) 

    def validate_threshold(self, input):
        """
        validates input to guarantee threshold between 0 and 9999

        Parameter:
        input: the entered threshold

        Return:
        boolean, indicates whether input is valid or not
        """

        if len(input) > 4:
            return False
        else:
            if len(input) == 0:
                # set button disabled because threshold should not be empty
                self.threshold_button.configure(state = ttk.DISABLED)
                return True
            try:
                int(input)
                # input is recognizable as int value
                self.threshold_button.configure(state = ttk.NORMAL)
                return True
            except ValueError:
                return False

    def update_results(self):
        """
        updates result based on new threshold
        """

        self.results_as_text, self.y_acceptance, self.y_rejection = c.update_verification_results(self.max_threshold.get())
        self.show_results()
