import keyboardcapture
import fileaccess
import verification
from sample import Sample

text_for_comparison = None
current_username = "Anonym"
current_sample = None
# keycodes for backspace, del, ->, <- (evtl. gar nicht alle nötig?)
forbidden_keycodes = (8, 46, 37, 39)


# keyboard recording
def process_keyboard_input(event, text, callback):
    # backspace
    if event.keycode in forbidden_keycodes:
        keyboardcapture.stop_recording()
        callback(False)
        return
    if text_for_comparison is not None:
        if text != text_for_comparison[:len(text)]:
            keyboardcapture.stop_recording()
            callback(True)
            return
    keyboardcapture.record_keyboard_entries(event)


def form_sample_from_entry(text, new_username, callback):
    # return key was pressed, keyboard recognition is over
    values_for_sample = keyboardcapture.extract_values_per_feature_and_chars(text)
    inputtime = keyboardcapture.inputtime
    keyboardcapture.stop_recording()
    global current_sample
    global current_username
    current_username = new_username
    current_sample = Sample(text, inputtime, current_username, values_for_sample)
    callback (2, current_sample.get_text_and_value_overview())       

def get_all_sample_identifier(callback):
    all_identifier = fileaccess.read_sample_identifier_from_file()
    callback (1, all_identifier)

def archive_current_sample(set_text_for_comparison, callback):
    fileaccess.write_sample_to_file(current_sample)
    delete_current_sample(set_text_for_comparison, callback)

def delete_current_sample(set_text_for_comparison, callback):
    global current_sample
    global text_for_comparison
    if set_text_for_comparison:
        text_for_comparison = current_sample.content
    else:
        text_for_comparison = None
    current_sample = None
    callback(0)

def verify(learnsample_identifier, testsample_identifier, encrypted, callback):
    learnsamples = fileaccess.read_samples_from_files(learnsample_identifier)
    testsamples = fileaccess.read_samples_from_files(testsample_identifier)
    #verification_output = verification.verify_per_threshold(learnsamples, testsamples, encrypted)
    #callback(3, verification_output)
    compared_values, results = verification.verify_per_threshold(learnsamples, testsamples, encrypted)
    if compared_values > 0:
        results_as_text = "Results\n\nAcceptance:\n"
        x_thresholds = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
        y_acceptance = list(results.values())
        y_rejection = []
        for k, v in results.items():
            y_rejection.append(100.00 - v)
            results_as_text += str(k) + "ms - " + str(v) + "%\n"
        results_as_text += "\nCompared time values: " + str(compared_values)
        print (str(y_rejection))
        callback(3, (x_thresholds, y_acceptance, y_rejection, results_as_text))
    else:
        callback(3)
    