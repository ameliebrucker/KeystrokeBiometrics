import controller.keyboardcapture as keyboardcapture
import controller.fileaccess as fileaccess
import controller.verification as verification
from model.sample import Sample

text_for_comparison = None
current_username = "Anonym"
current_sample = None
# keycodes for backspace, del, arrow keys (->, <-)
forbidden_keycodes = (8, 46, 37, 39)

def process_keyboard_input(event, text, callback):
    """
    processes event from keyboard input, detects incorrect characters and and reacts to them

    Parameter:
    event: keystroke event from typing in text field
    text: text field content at the time of function call
    callback: callback function after detecting invalid character with parameter whether content comparison failed

    Return:
    result of character validation via callback
    """

    if event.keycode in forbidden_keycodes:
        # input contains forbidden characters
        keyboardcapture.stop_recording()
        return callback(False)
    if text_for_comparison is not None:
        if text != text_for_comparison[:len(text)]:
            # input does not match required content
            keyboardcapture.stop_recording()
            return callback(True)
    # input accepted, record keystrokes
    keyboardcapture.record_keyboard_entries(event)


def form_sample_from_entry(content, new_username, callback):
    """
    creates new sample from collected data and terminates current input

    Parameter:
    content: text field content at the time of function call
    new_username: username specified by the user for the current entry
    callback: callback function for page change after sample creation 

    Return:
    next page number, overview of content and values from new sample via callback
    """

    if len(content) > 0:
        values_for_sample, inputtime = keyboardcapture.extract_values_per_feature_and_chars(content)
        global current_sample
        global current_username
        current_username = new_username
        current_sample = Sample(content, inputtime, current_username, values_for_sample)
        # show page 2 with overview of sample content and values
        callback (2, current_sample.get_content_and_values_overview())
    else:
        keyboardcapture.stop_recording()
        callback(2)    

def get_all_sample_identifier(callback):
    """
    retrieves identifiers for archived samples

    Parameter:
    callback: callback function for showing new page with all identifiers

    Return:
    next page number, identifiers for archived samples via callback
    """

    all_identifier = fileaccess.read_sample_identifier_from_file()
    # show page 1 with identifier
    callback (1, all_identifier)

def archive_current_sample(set_text_for_comparison, callback):
    """
    archives current sample and calls delete_current_sample function

    Parameter:
    set_text_for_comparison: boolean, indicates whether current content should be used as comparison text
    callback: callback function for page change to pass on to delete_current_sample function

    Precondition:
    current_sample is not None (form_sample_from_entry() has been executed)
    """
    
    fileaccess.write_sample_to_file(current_sample)
    delete_current_sample(set_text_for_comparison, callback)

def delete_current_sample(set_text_for_comparison, callback):
    """
    prepares new input by removing old data (current sample) from intermediate storage

    Parameter:
    set_text_for_comparison: boolean, indicating whether current content should be used as comparison text
    callback: callback function for page change after deleting current sample

    Return:
    next page number via callback
    """
    
    global current_sample
    global text_for_comparison
    if set_text_for_comparison:
        text_for_comparison = current_sample.content
    else:
        text_for_comparison = None
    current_sample = None
    # show page 0
    callback(0)

def verify(learnsample_identifiers, testsample_identifiers, encrypted, callback):
    """
    performs verification process and provides values for displaying result as text and diagrams

    Parameter:
    learnsample_identifiers: list of learsample identifiers
    testsample_identifiers: list of testsample identifiers
    encrypted: boolean, indicating whether verification process should be performed with encrypted testsamples
    callback: callback function for page change and result data transfer

    Return:
    next page number, verification results as text and chart values:
        list of x values for acceptance diagram and rejection diagram
        list of y values for acceptance diagram
        list of y values for rejection diagram,
    via callback

    Precondition:
    learnsamples and testsamples from identifiers have been archived
    """

    # get archived learnsamples and testsamples by identifiers
    learnsamples = fileaccess.read_samples_from_files(learnsample_identifiers)
    testsamples = fileaccess.read_samples_from_files(testsample_identifiers)
    # perform verification process
    compared_values, results = verification.verify_per_threshold(learnsamples, testsamples, encrypted)
    if compared_values > 0:
        # samples contained comparable data
        # set thresholds as number between 0 and 1 as list
        x_thresholds = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
        # set acceptance and rejection values as list
        y_acceptance = list(results.values())
        y_rejection = []

        acceptance_as_text = "\nAcceptance:\n"
        rejection_as_text = "\nRejection:\n"
        index = 0
        for k, v in results.items():
            # fill list of rejection values based on results
            rejection_value = round(100 - v, 2)
            y_rejection.append(rejection_value)
            # append acceptance and rejection values to text
            acceptance_as_text += f"{x_thresholds[index]} ({k}ms) - {v}%\n"
            rejection_as_text += f"{x_thresholds[index]} ({k}ms) - {rejection_value}%\n"
            index += 1
        results_as_text = f"Results\n{acceptance_as_text}{rejection_as_text}\nCompared time values: {compared_values}"
        # show page 3 with results as text and chart data
        callback(3, (results_as_text, x_thresholds, y_acceptance, y_rejection))
    else:
        # show page 3
        callback(3)
    