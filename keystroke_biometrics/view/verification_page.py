import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import controller.application_logic as c

class VerificationPage(Page):
    """
    A class for representing the verification page of the user interface

    Attributes (Object)
    checked_identifiers: dictionary with identifiers as key and boolean whether they are selected as values
    encryption_check: boolean, indicates whether learnsamples should be treated as encrypted
    tooltip_frame: label with tip for selection

    Methods
    starting_verification(callback): summarizes selected samples and starts verification process
    """

    def __init__(self, root, identifier):
        super().__init__(root, "Verification", True)
        mainframe = ttk.Frame(self)
        if not identifier:
            mainframe.pack(pady=(15, 0))
            # add instructions
            ttk.Label(mainframe, text="No samples", font=root.font14bold).pack(anchor = ttk.W, pady=(0, 8))
            ttk.Label(mainframe, text="How do I add samples?").pack(anchor = ttk.W)
            ttk.Label(mainframe, text="1. Navigate to the \"Recording samples\" page (free or fixed text - it's your choice)").pack(anchor = ttk.W)
            ttk.Label(mainframe, text="2. Type your text in the input field, finish by pressing the enter key").pack(anchor = ttk.W)
            ttk.Label(mainframe, text="3. On the recording results page, press the \"Save this sample\" button").pack(anchor = ttk.W)
            ttk.Label(mainframe, text="4. Return to this page").pack(anchor = ttk.W)
        else:
            mainframe.pack()
            # add instruction
            ttk.Label(mainframe, text="Select samples", font=root.font14bold).pack(anchor = ttk.W)
            # create dict from identifier with default selection False
            self.checked_identifiers = {identifier[i]: (ttk.BooleanVar(value=False), ttk.BooleanVar(value=False)) for i in range(0, len(identifier), 1)}
            sample_selection = ttk.Frame(mainframe)
            sample_selection.pack()
            # add learnsample overview
            learnsample_frame = ttk.Frame(sample_selection)
            learnsample_frame.pack(side=ttk.LEFT, padx=(0, 2))
            ttk.Label(learnsample_frame, text="Learnsamples for verification process", font=root.font10).pack(anchor=ttk.W)
            learnsamples_overview = ScrolledText (learnsample_frame, cursor='arrow', height=15, width=68)
            learnsamples_overview.configure(state = ttk.DISABLED)
            learnsamples_overview.pack()
            # add testsample overview
            testsample_frame = ttk.Frame(sample_selection)
            testsample_frame.pack(side=ttk.RIGHT, padx=(2, 0))
            ttk.Label(testsample_frame, text="Testsamples for verification process", font=root.font10).pack(anchor=ttk.W)
            testsamples_overview = ScrolledText (testsample_frame, cursor='arrow', height=15, width=68)
            testsamples_overview.configure(state = ttk.DISABLED)
            testsamples_overview.pack()
            # add checkbox lists with identifiers
            for k, v in self.checked_identifiers.items():
                learnsamples_overview.window_create(ttk.END, window=ttk.Checkbutton(learnsamples_overview, text=k, variable=v[0], onvalue=True, offvalue=False, width=63))
                testsamples_overview.window_create(ttk.END, window=ttk.Checkbutton(testsamples_overview, text=k, variable=v[1], onvalue=True, offvalue=False, width=63))       
            # add tooltip for selection
            self.tooltip_frame = ttk.Frame (mainframe)
            self.tooltip_frame.pack(anchor=ttk.E)
            tooltip_border = ttk.Labelframe(self.tooltip_frame, bootstyle=ttk.DANGER, text=" ! ")
            tooltip_border.pack(pady=(0, 2))
            tooltip = ttk.Label (tooltip_border, text = "Choose at least one sample per group.", foreground="red")
            tooltip.pack()
            submit_frame = ttk.Frame(mainframe)
            submit_frame.pack()
            # add encryption check
            self.encryption_check = ttk.BooleanVar(value=False)
            checkbox_encryption = ttk.Checkbutton(submit_frame, text="Encrypt testsamples for verification", variable=self.encryption_check, onvalue=True, offvalue=False, style="LargeCheckbutton.TCheckbutton")
            checkbox_encryption.pack(pady=(0, 6))
            # add button for starting verification
            ttk.Button(submit_frame, text='Start verification process', command= lambda: self.starting_verification(root.change_page), style="SubmitButton.TButton").pack(expand=True, fill=ttk.X)

    def starting_verification(self, callback):
        """
        summarizes selected samples and starts verification process

        Parameter:
        callback: callback passed to verification function
        """

        selected_learnsamples = []
        selected_testsamples = []
        for k, v in self.checked_identifiers.items():
            if v[0].get():
                # box is checked: selected as learnsample
                selected_learnsamples.append(k)
            if v[1].get():
                # box is checked: selected as testsample
                selected_testsamples.append(k)
        if not selected_learnsamples or not selected_testsamples:
            # nothing selected, show warning
            self.tooltip_frame.configure(bootstyle=ttk.DANGER)
        else:
            c.verify(selected_learnsamples, selected_testsamples, self.encryption_check.get(), callback)