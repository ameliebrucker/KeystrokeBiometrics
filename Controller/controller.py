import keyboardcapture
import fileaccess
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
    callback(3)