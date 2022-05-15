import tkinter as tk

from view.recording_page import RecordingPage
from view.verification_page import VerificationPage
from view.recording_results_page import RecordingResultsPage
from view.verification_results_page import VerificationResultsPage

class ApplicationUI (tk.Tk):
    """
    A class for representing the application of the user interface

    Attributes (Object)
    content: string, total text entered

    Methods
    get_short_identifier(): gives 
    """

    def __init__(self):
        """
        initializes page, therefore adds components to root component

        Parameter:
        title: title of the application
        state: state of window dimension
        all_page_classes: tuple of all pages included in application
        page_number_from_header: number of current pagegroup (recording or verification) based on navigation buttons from header
        current_page: currently shown page

        Methods
        change_page(page_number, data): changes currently shown page
        """

        super().__init__()
        # set title and window dimensions
        self.title("Keystroke Biometrics")
        self.state("zoomed")
        # create page tracking for view changes
        self.all_page_classes = (RecordingPage, VerificationPage, RecordingResultsPage, VerificationResultsPage)
        self.page_number_from_header = tk.IntVar()
        # initialize start page
        self.page_number_from_header.set(0)
        self.current_page = self.all_page_classes[0](self)
        self.current_page.pack(fill='x')

    def change_page(self, page_number, data = None):
        """
        changes currently shown page

        Parameter:
        page_number: number of new page
        data: data, which should be transfered to page component
        """

        self.current_page.destroy()
        if data is None:
            self.current_page = self.all_page_classes[page_number](self)
        else:
            self.current_page = self.all_page_classes[page_number](self, data)
        self.current_page.pack(fill='x')

#TODO alle daten in input_data übergeben (username, vergleich content)

def run_application():
    root = ApplicationUI()
    root.mainloop()