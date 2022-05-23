import tkinter as tk

from view.recording_page import RecordingPage
from view.template_text_page import TemplateTextPage
from view.verification_page import VerificationPage
from view.recording_results_page import RecordingResultsPage
from view.verification_results_page import VerificationResultsPage

class Application (tk.Tk):
    """
    A class for representing the application of the user interface

    Attributes (Object)
    title: title of the application
    state: state of window dimension
    all_page_classes: tuple of all pages included in application
    page_from_header: name of current page based on navigation buttons from header
    current_page: currently shown page

    Methods
    change_page(self, page_number, data): changes currently shown page
    """

    def __init__(self):
        super().__init__()
        # set title and window dimensions
        self.title("Keystroke Biometrics")
        self.state("zoomed")
        # create page tracking for view changes
        self.all_page_classes = {
            "RecordingPage" : RecordingPage,
            "TemplateTextPage" : TemplateTextPage,
            "VerificationPage" : VerificationPage,
            "RecordingResultsPage" : RecordingResultsPage,
            "VerificationResultsPage": VerificationResultsPage}
        self.page_from_header = tk.StringVar()
        # initialize start page
        self.page_from_header.set("RecordingPage")
        self.current_page = self.all_page_classes["RecordingPage"](self)
        self.current_page.pack(fill='x')

    def change_page(self, page, data = None):
        """
        changes currently shown page

        Parameter:
        page: class name of new page as string
        data: data, which should be transfered to page component
        """

        self.current_page.destroy()
        if data is None:
            self.current_page = self.all_page_classes[page](self)
        else:
            self.current_page = self.all_page_classes[page](self, data)
        self.current_page.pack(fill='x')

def start_application():
    """
    starts application by showing user interface
    """

    root = Application()
    root.mainloop()