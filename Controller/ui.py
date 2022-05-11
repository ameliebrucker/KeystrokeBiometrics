from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from tkinter import *
from tkinter.scrolledtext import ScrolledText

#from keystroke_biometrics.controller.controller import *
# from Controller import controller as c
#import Controller.controller as c
import controller as c

# styles
# ??????? hinzufügen ????

class ApplicationUI (Tk):
    def __init__(self):
        super().__init__()
        self.title("Keystroke Biometrics")
        # self.geometry("500x400")
         # self.state('zoomed')

        # track current page
        self.all_page_classes = (RecordingPage, VerificationPage, RecordingResultsPage, VerificationResultsPage)
        self.page_number_from_header = IntVar()
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

class Page(Frame):
    def __init__(self, root, page_name, view_change=False):
       super().__init__(root)
       header = Frame(self)
       header.pack(pady=20, padx=20, side= TOP, anchor="w")
       Label (self, text = page_name, font=('Helvetica', 18, "bold")).pack()
       if view_change:
           Radiobutton(header, text="Recording Samples", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=root.change_page,value=0).grid(row=0, column=1)
           Radiobutton(header, text="Verification", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=lambda: c.get_all_sample_identifier(root.change_page),value=1).grid(row=0, column=2)

#TODO alle daten in input_data übergeben (username, vergleich content)
class RecordingPage(Page):
    def __init__(self, root, input_data = None):
        super().__init__(root, "Recording Samples", True)

        # username frame
        username_frame = Frame(self)
        username_frame.pack()
        Label(username_frame, text="Username: ").grid(row=0)
        self.username = StringVar(value=c.current_username)
        self.username_entry = Entry(username_frame, text=self.username)
        self.username_entry.bind("<Key>", self.limit_username_length)
        self.username_entry.grid(row=0, column=1)

        #entry field for keystroke recognition
        self.input_text_box = Text(self, height=12, width=80)
        #text_box.bind("<KeyPress>", c.validate_keyboard_entries)
        self.input_text_box.bind("<KeyPress>", lambda e: c.process_keyboard_input(e, self.input_text_box.get(1.0, "end-1c"), self.input_validation_failed))
        self.input_text_box.bind("<KeyRelease>", lambda e: c.process_keyboard_input(e, self.input_text_box.get(1.0, "end-1c"), self.input_validation_failed))
        #text_box.bind("<KeyRelease>",c.form_sample_from_entry)
        # zeichenkette bis zu return taste
        self.input_text_box.bind("<Return>", lambda e: c.form_sample_from_entry(self.input_text_box.get(1.0, "end-1c"), self.username.get(), root.change_page))
        # text_box = Entry(self)
        self.input_text_box.pack()

        #required text
        if c.text_for_comparison is not None:
            self.required_text_tip = Label (self, text="Required text input: \"" + c.text_for_comparison + "\"")
            self.required_text_tip.pack()

        #tooltip
        self.tooltip = Label (self, text = "Please type your sample text as fluent as possible in the box above. Avoid deleting characters or changing the cursor position. Finish your entry by pressing the enter key.")
        self.tooltip.pack()
    
    def limit_username_length(self, event):
        #limit to 30 characters to avoid problems with long input
        if len(self.username_entry.get()) > 29:
            self.username_entry.delete(29, END)

    def input_validation_failed(self, comparison_failed):
        self.input_text_box.delete("1.0","end")
        if comparison_failed:
            self.required_text_tip.config(bg= "red")
        else:
            self.tooltip.config(bg="red")
        

class VerificationPage(Page):
    def __init__(self, root, input_data_identifier):
        super().__init__(root, "Verification", True)
        self.input_data_identifier = input_data_identifier
        self.learnsamples_identifier = []
        self.testsamples_identifier = []

        #elements in view
        sample_selection = Frame(self)
        sample_selection.pack()
        Label(sample_selection, text="Learnsamples for verification process").grid(row=0, column=0)
        Label(sample_selection, text="Testsamples for verification process").grid(row=0, column=1)
        self.learnsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=12, width=30)
        self.testsamples_overview = ScrolledText (sample_selection, cursor='arrow', height=12, width=30)
        self.learnsamples_overview.grid(row=1, column=0)
        self.testsamples_overview.grid(row=1, column=1)

        self.fill_with_input_data()

        encryption_check = BooleanVar(value=False)
        checkbox_encryption = Checkbutton(self, text="Verification process should be done with encrypted testsamples", variable=encryption_check, onvalue=True, offvalue=False)
        checkbox_encryption.pack()
        Button(self, text='Start verification process', command= lambda: c.verify(self.get_selected_learnidentifier(), self.get_selected_testidentifier(), True, root.change_page)).pack()
            
    def fill_with_input_data(self):
        index = 0
        for sample in self.input_data_identifier:
            # new entry in list with default value "" (unchecked)
            self.learnsamples_identifier.append(StringVar(value=""))
            self.testsamples_identifier.append(StringVar(value=""))
            #TODO put windows untereinander
            self.learnsamples_overview.window_create(END, window=Checkbutton(self.learnsamples_overview, text=sample, variable=self.learnsamples_identifier[index], onvalue=sample, offvalue=""))
            self.testsamples_overview.window_create(END, window=Checkbutton(self.testsamples_overview, text=sample, variable=self.testsamples_identifier[index], onvalue=sample, offvalue=""))
            # , variable=output_data_testsamples[index], onvalue=sample, offvalue=""
            index += 1
            
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
        
       


class RecordingResultsPage(Page):
    def __init__(self, root, input_data_content_and_values):
        super().__init__(root, "Recording Results")

        # textfield for displaying entered text
        result_text_box = ScrolledText(self, height=12, width=80)
        result_text_box.insert(INSERT, input_data_content_and_values)
        result_text_box.configure(state ='disabled')
        result_text_box.pack()

        # checkbox keep entry as reference for next entrys
        reference_entry_check = BooleanVar(value=False)
        if c.text_for_comparison is not None:
            reference_entry_check.set(True)
        checkbox_reference_entry = Checkbutton(self, text="Keep this text as validation reference for next entry", variable=reference_entry_check, onvalue=True, offvalue=False)
        checkbox_reference_entry.pack()

        # button group
        button_group = Frame(self)
        button_group.pack()
        Button(button_group, text='Delete this record', command=lambda: c.delete_current_sample(reference_entry_check.get(), root.change_page)).grid(row=0, column=0)
        Button(button_group, text='Save this record', command=lambda: c.archive_current_sample(reference_entry_check.get(), root.change_page)).grid(row=0, column=1)

class VerificationResultsPage(Page):
    def __init__(self, root, input_data):
        super().__init__(root, "Verification Results")

#if __name__ == "__main__":
root = ApplicationUI()
root.mainloop()