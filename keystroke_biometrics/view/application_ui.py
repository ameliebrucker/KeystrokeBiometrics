import tkinter as tk
import ttkbootstrap as ttk

from view.recording_page import RecordingPage
from view.template_text_page import TemplateTextPage
from view.verification_page import VerificationPage
from view.recording_results_page import RecordingResultsPage
from view.verification_results_page import VerificationResultsPage

class Application (ttk.tk.Tk):
    """
    A class for representing the application of the user interface

    Attributes (Object)
    title: title of the application
    style: style object with style aspects for application
    state: state of window dimension
    font18: font in size 18 for styling
    font14bold: bold font in size 14 for styling
    font10: font in size 10 for styling
    all_page_classes: tuple of all pages included in application
    page_from_header: name of current page based on navigation buttons from header
    current_page: currently shown page

    Methods
    change_page(self, page, data): changes currently shown page
    """

    def __init__(self):
        super().__init__()
        # set title and window dimensions
        self.title("Keystroke Biometrics")
        self.style = ttk.Style("flatly")
        self.state("zoomed")
        # set fonts
        self.font18 = ttk.font.Font(self, family="Microsoft JhengHei UI", size=18)
        self.font14bold = ttk.font.Font(self, family="Microsoft JhengHei UI", size=14, weight="bold")
        self.font10 = ttk.font.Font(self, family="Microsoft JhengHei UI", size=10)
        # set styles
        self.style.configure("TLabel", font=self.font10)
        self.style.configure("Headline.TLabel", font=self.font18)
        self.style.configure("MediumHeadline.TLabel", font=self.font14bold)
        self.style.configure("TooltipLabel.TLabel", foreground="red", font=self.font10)
        self.style.configure("SubmitButton.TButton", font=self.font10)
        self.style.configure("LargeCheckbutton.TCheckbutton", font=self.font10)
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
        self.current_page.pack(fill=ttk.X)

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