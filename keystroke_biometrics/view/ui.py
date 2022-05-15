import tkinter as tk

from view.recording_page import RecordingPage
from view.verification_page import VerificationPage
from view.recording_results_page import RecordingResultsPage
from view.verification_results_page import VerificationResultsPage

#from keystroke_biometrics.controller.controller import *
# from Controller import controller as c
#import Controller.controller as c

# styles
# ??????? hinzufügen ????

class ApplicationUI (tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Keystroke Biometrics")
        # self.geometry("500x400")
        # self.state('zoomed')

        # track current page, number 0-4
        self.all_page_classes = (RecordingPage, VerificationPage, RecordingResultsPage, VerificationResultsPage)
        self.page_number_from_header = tk.IntVar()
        self.page_number_from_header.set(0)

        # initialize start page
        self.current_page = self.all_page_classes[0](self)
        self.current_page.pack(fill='x')

    def change_page(self, page_number = None, data = None):
        if page_number is None:
            page_number = self.page_number_from_header.get()
        self.current_page.destroy()
        #if data is None:
            #self.current_page = self.all_page_classes[page_number](self)
        #else:
        self.current_page = self.all_page_classes[page_number](self, data)
        self.current_page.pack(fill='x')

#TODO alle daten in input_data übergeben (username, vergleich content)

#if __name__ == "__main__":
root = ApplicationUI()
root.mainloop()