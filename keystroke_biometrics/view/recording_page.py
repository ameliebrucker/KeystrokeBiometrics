import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
from view.page import Page
import controller.application_logic as c

class RecordingPage(Page):
    """
    A class for representing the recording page of the user interface

    Attributes (Object)
    input_textbox: textbox in which keystrokes are recorded
    required_text_border: frame for border around required text
    tooltip_frame: frame with tip on how to type

    Methods
    set_cursor_to_end(): sets cursor to the end of input_textbox
    limit_username_length(event): limits username to 30 characters
    input_validation_failed(comparison_failed): displays information about failing input validation
    """

    def __init__(self, root, fixed_text = False):
        # set default title
        title = "Recording (free text)"
        if fixed_text:
            # change title for fixed text
            title = "Recording (fixed text)"
        super().__init__(root, title, True)
        mainframe = ttk.Frame(self)
        mainframe.pack()
        # add username entry field + label
        username_frame = ttk.Frame(mainframe)
        username_frame.pack(anchor = ttk.E)
        ttk.Label(username_frame, text="Username: ").grid(row=0)
        username = ttk.StringVar(value=c.current_username)
        # limit username length by registering validation function
        limit_length_command = (root.register(self.limit_username_length), '%P')
        username_entry = ttk.Entry(username_frame, text=username, validate="key", validatecommand=limit_length_command)
        username_entry.bind("<FocusOut>", lambda e: c.set_username(username.get()))
        username_entry.grid(row=0, column=1)
        # add instructions
        ttk.Label(mainframe, text="Type your text", style="MediumHeadline.TLabel").pack(anchor = ttk.W)
        ttk.Label(mainframe, text="Your keystrokes will be recorded. Finish by pressing the enter key.").pack(anchor = ttk.W)
        if fixed_text:
            # add label and button for required text 
            required_text_header = ttk.Frame(mainframe, bootstyle=ttk.PRIMARY)
            required_text_header.pack(expand=True, fill=ttk.X, pady=(5, 0))
            # configure spacing for columns
            required_text_header.grid_columnconfigure(1, weight=1)
            ttk.Label (required_text_header, text="Required text input:", bootstyle=ttk.INVERSE + ttk.PRIMARY).grid(row=0, column=0, sticky=ttk.W, padx=5)
            ttk.Button(required_text_header, text="Change template text", command=lambda:root.change_page("TemplateTextPage"), bootstyle=ttk.OUTLINE).grid(row=0, column=1, sticky=ttk.E)
            # add border frame for required text
            self.required_text_border = ttk.Frame(mainframe, bootstyle=ttk.PRIMARY)
            self.required_text_border.pack(fill=ttk.X, pady=(0, 5))
            # add scrollable widget for required text 
            required_text_box = ScrolledText(self.required_text_border, height=3)
            required_text_box.pack(fill=ttk.X, padx=1, pady=1)
            required_text_box.insert(ttk.INSERT, c.template_text)
            required_text_box.configure(state=ttk.DISABLED)            
        # add textbox for keystroke recognition
        input_textbox_border = ttk.Frame(mainframe, bootstyle=ttk.LIGHT)
        input_textbox_border.pack(fill=ttk.X)
        self.input_textbox = ttk.Text(input_textbox_border, height=12, wrap=ttk.WORD)
        self.input_textbox.focus_set()
        self.input_textbox.bind("<KeyPress>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), fixed_text, self.input_validation_failed))
        self.input_textbox.bind("<KeyRelease>", lambda e: c.process_keyboard_input(e, self.input_textbox.get(1.0, "end-1c"), fixed_text, self.input_validation_failed))
        # set return key as input exit
        self.input_textbox.bind("<Return>", lambda e: c.form_sample_from_entry(self.input_textbox.get(1.0, "end-1c"), fixed_text, root.change_page))
        # prevent user from changing cursor position
        self.input_textbox.bind("<Button>", lambda e: self.set_cursor_to_end())
        self.input_textbox.pack(expand=True, fill=ttk.X, padx=1, pady=1)
        # add tooltip on how to type properly
        self.tooltip_frame = ttk.Frame(mainframe)
        self.tooltip_frame.pack()
        tooltip_border = ttk.Labelframe(self.tooltip_frame, bootstyle=ttk.DANGER, text=" ! ")
        tooltip_border.pack(pady=(0, 2))
        tooltip = ttk.Label(tooltip_border, text = "Do not delete characters, paste a copied text or change the cursors position while entering your text.", style="TooltipLabel.TLabel")
        tooltip.pack()

    def set_cursor_to_end(self):
        """
        sets cursor to the end of input_textbox to prevent user from writing to another position
        """

        self.input_textbox.focus_set()
        self.input_textbox.mark_set(ttk.INSERT, ttk.END)
        # prevent default behaviour of setting cursor to clicked position
        return("break")
    
    def limit_username_length(self, input):
        """
        validates input to limit username to 20 characters

        Parameter:
        input: the entered username

        Return:
        boolean, indicates whether input is valid or not
        """

        if len(input) > 20:
            return False
        else:
            return True

    def input_validation_failed(self, comparison_failed):
        """
        displays information about failing input validation for user

        Parameter:
        comparison_failed: boolean, indicates whether the comparison with the template text failed
        """

        # delete corrupted content completely
        self.input_textbox.delete("1.0", ttk.END)
        if comparison_failed:
            # highlight required text border
            self.required_text_border.configure(bootstyle=ttk.DANGER)
        else:
            # highlight tooltip frame
            self.tooltip_frame.configure(bootstyle=ttk.DANGER)
            
        