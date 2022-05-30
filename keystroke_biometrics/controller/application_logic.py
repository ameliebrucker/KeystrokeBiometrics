import controller.keyboardcapture as keyboardcapture
import controller.fileaccess as fileaccess
import controller.verification as verification
from model.sample import Sample

template_text = ""
current_username = "Anonym"
current_sample = None
# keysymbols for backspace, del, arrow keys (->, <-)
forbidden_keysyms = ("BackSpace", "Delete", "Right", "Left")

def process_keyboard_input(event, text, comparison, callback):
    """
    processes event from keyboard input, detects incorrect characters and reacts to them

    Parameter:
    event: keystroke event from typing in text field
    text: text field content at the time of function call
    comparison: boolean, indicates whether input text should be compared with template text
    callback: callback function after detecting invalid character with parameter whether content comparison failed
    """

    if event.keysym in forbidden_keysyms:
        # input contains forbidden characters
        keyboardcapture.stop_recording()
        return callback(False)
    if comparison:
        if text != template_text[:len(text)]:
            # input does not match required content
            keyboardcapture.stop_recording()
            return callback(True)
    # input accepted, record keystrokes
    keyboardcapture.record_keyboard_entries(event)


def form_sample_from_entry(content, fixed_text_recording, callback):
    """
    creates new sample from collected data and terminates current input

    Parameter:
    content: text field content at the time of function call
    fixed_text_recording: boolean, indicates whether sample comes from fixed text recording page
    callback: callback function for page change after sample creation 
    """

    # if recording was with fixed text, check if content length matches template text length
    if len(content) > 0 and (not fixed_text_recording or len(content) is len(template_text)):
        values_for_sample, inputtime = keyboardcapture.extract_values_per_feature_and_chars(content)
        if not values_for_sample:
            # no recorded values, show recording results page
            return callback("RecordingResultsPage", (fixed_text_recording, None))
        global current_sample
        current_sample = Sample(content, inputtime, current_username, values_for_sample)
        # show recording results page with overview of sample content and values
        callback ("RecordingResultsPage", (fixed_text_recording, current_sample.get_content_and_values_overview()))
    else:
        keyboardcapture.stop_recording()
        # show recording results page
        callback("RecordingResultsPage", (fixed_text_recording, None))    

def set_template_text(text, callback):
    """
    sets given text as template text

    Parameter:
    text: text for template text
    callback: callback function after setting template text
    """

    global template_text
    # remove \n since it is reserved for finishing entries
    template_text = text.replace("\n","")
    # show recording page with template text
    callback("RecordingPage", True)

def set_username(username):
    """
    sets username

    Parameter:
    username: name to be set as username
    """

    global current_username
    current_username = username
    

def get_all_sample_identifier(callback):
    """
    retrieves identifiers for archived samples

    Parameter:
    callback: callback function for showing page with all identifiers
    """

    all_identifiers = fileaccess.read_sample_identifier_from_file()
    # show verification page with identifiers
    callback ("VerificationPage", all_identifiers)

def archive_current_sample(navigate_to_fixed_text_recording, callback):
    """
    archives current sample and calls delete_current_sample() function

    Parameter:
    navigate_to_fixed_text_recording: boolean, indicates whether callback should navigate to fixed text recording page
    callback: callback function for page change to pass on to delete_current_sample() function

    Precondition:
    current_sample is not None (form_sample_from_entry() has been executed)
    """
    
    fileaccess.write_sample_to_file(current_sample)
    delete_current_sample(navigate_to_fixed_text_recording, callback)

def delete_current_sample(navigate_to_fixed_text_recording, callback):
    """
    prepares new input by removing old data (current sample) from intermediate storage

    Parameter:
    navigate_to_fixed_text_recording: boolean, indicates whether callback should navigate to fixed text recording page
    callback: callback function for page change after deleting current sample
    """
    
    global current_sample
    current_sample = None
    # show recording page with or without fixed text
    callback("RecordingPage", navigate_to_fixed_text_recording)

def verify(learnsample_identifiers, testsample_identifiers, encrypted, callback):
    """
    performs verification process and provides values for displaying result as text and diagrams

    Parameter:
    learnsample_identifiers: list of learsample identifiers
    testsample_identifiers: list of testsample identifiers
    encrypted: boolean, indicating whether verification process should be performed with encrypted testsamples
    callback: callback function for page change and result data transfer

    Precondition:
    learnsamples and testsamples from identifiers have been archived
    """

    # get archived learnsamples and testsamples by identifiers
    learnsamples = fileaccess.read_samples_from_files(learnsample_identifiers)
    testsamples = fileaccess.read_samples_from_files(testsample_identifiers)
    # perform verification process
    compared_values, max_threshold, euklidean_distance_dict = verification.verify_samples(learnsamples, testsamples, encrypted)
    results = verification.results_per_threshold(euklidean_distance_dict, compared_values, max_threshold)
    if results is not None:
        # show verification results page with results
        callback("VerificationResultsPage", results)
    else:
        # show verification results page without results
        callback("VerificationResultsPage")
    