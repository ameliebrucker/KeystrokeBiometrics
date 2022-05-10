from tkinter import *
from tkinter import font
from tkinter.scrolledtext import ScrolledText

import controller as c

# styles
# ??????? hinzufügen ????

class ApplicationUI (Tk):
    def __init__(self):
        Tk.__init__(self)
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
       Frame.__init__(self, root)
       header = Frame(self)
       header.pack(pady=20, padx=20, side= TOP, anchor="w")
       Label (self, text = page_name, font=('Helvetica', 18, "bold")).pack()
       if view_change:
           Radiobutton(header, text="Recording Samples", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=root.change_page,value=0).grid(row=0, column=1)
           Radiobutton(header, text="Verification", indicatoron = 0, width = 20, variable=root.page_number_from_header, command=root.change_page,value=1).grid(row=0, column=2)

class RecordingPage(Page):
    def __init__(self, root, input_data = None):
        Page.__init__(self, root, "Recording Samples", True)

        # username frame
        username_frame = Frame(self)
        username_frame.pack()
        Label(username_frame, text="Username: ").grid(row=0)
        username = StringVar(value=c.current_username)
        Entry(username_frame, text=username).grid(row=0, column=1)

        #entry field for keystroke recognition
        text_box = Text(self, height=12, width=80)
        text_box.bind("<KeyPress>", c.form_sample_from_entry)
        text_box.bind("<KeyRelease>", c.form_sample_from_entry)
        # zeichenkette bis zu return taste
        text_box.bind("<Return>", lambda event: c.form_sample_from_entry(event, root.change_page, username.get(), text_box.get(1.0, "end-1c")))
        # text_box = Entry(self)
        text_box.pack()

        #tooltip
        Label (self, text = "Please type your sample text as fluent as possible in the box above. Finish your entry by pressing the enter key.").pack()

    def validate_text_input(self):
        text_for_comparison = c.text_for_comparison

        

class VerificationPage(Page):
    def __init__(self, root, input_data = None):
        Page.__init__(self, root, "Verification", True)

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
        Button(self, text='Start verification process').pack()

        
        # c = test_list.count(item)
        # for i in range(c):
            # test_list.remove(item)

    def fill_with_input_data(self):
        input_data_samples = c.get_all_sample_identifier()
        output_data_learnsamples = []
        output_data_testsamples = []

        index = 0
        for sample in input_data_samples:
            # new_default_learn_var = StringVar(value="")
            # new_default_test_var = StringVar(value="")
            output_data_learnsamples.append(StringVar(value=""))
            output_data_testsamples.append(StringVar(value=""))
            #TODO put windows untereinander
            self.learnsamples_overview.window_create(END, window=Checkbutton(self.learnsamples_overview, text=sample, variable=output_data_learnsamples[index], onvalue=sample, offvalue=""))
            self.testsamples_overview.window_create(END, window=Checkbutton(self.testsamples_overview, text=sample, variable=output_data_testsamples[index], onvalue=sample, offvalue=""))
            # , variable=output_data_testsamples[index], onvalue=sample, offvalue=""
            index += 1

       


class RecordingResultsPage(Page):
    def __init__(self, root, input_data):
        Page.__init__(self, root, "Recording Results", input_data)

        # textfield for displaying entered text
        result_text_box = ScrolledText(self, height=12, width=80)
        result_text_box.insert(INSERT, input_data)
        result_text_box.configure(state ='disabled')
        result_text_box.pack()

        # checkbox keep entry as reference for next entrys
        # TODO keep this value checked/unchecked even after page change
        reference_entry_check = BooleanVar(value=False)
        checkbox_reference_entry = Checkbutton(self, text="Keep this text as validation reference for next entry", variable=reference_entry_check, onvalue=True, offvalue=False)
        # checkbox_reference_entry.select()
        checkbox_reference_entry.pack()

        # button group
        button_group = Frame(self)
        button_group.pack()
        Button(button_group, text='Delete this record').grid(row=0, column=0)
        Button(button_group, text='Save this record').grid(row=0, column=1)

class VerificationResultsPage(Page):
    def __init__(self, root, input_data):
        Page.__init__(self, root, "Verification Results", input_data)

root = ApplicationUI()
root.mainloop()