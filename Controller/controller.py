import keyboardcapture

from sample import Sample

text_for_comparison = None
current_username = "Anonym"
current_sample = None
# keycodes for backspace, del, ->, <- (evtl. gar nicht alle nötig?)
forbidden_keycodes = (8, 46, 37, 39)

# keyboard recording

"""
def form_sample_from_entry(event, callback = None, text="", new_username="Anonym"):
    if callback is None:
        keyboardcapture.record_keyboard_entries(event)
    else:
        # return key was pressed, keyboard recognition is over
        values_for_sample = keyboardcapture.extract_values_per_feature_and_chars(text)
        inputtime = keyboardcapture.inputtime
        keyboardcapture.stop_recording()
        global current_sample
        global current_username
        current_username = new_username
        current_sample = Sample(text, inputtime, current_username, values_for_sample)
        callback (2, current_sample.get_text_and_value_overview())
"""

def process_keyboard_input(event, text, callback):
    # backspace
    if event.keycode in forbidden_keycodes:
        callback(False)
    if text_for_comparison is not None:
        if text != text_for_comparison[:len(text)]:
            callback(True)
            keyboardcapture.stop_recording()
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

def get_all_sample_identifier():
    if current_sample is not None:
        return("Username41", current_sample.get_short_identifier())
    else:
        return("Username41",)

def archive_current_sample(set_text_for_comparison):
    return ""

def delete_current_sample(set_text_for_comparison, callback):
    global current_sample
    global text_for_comparison
    if set_text_for_comparison:
        text_for_comparison = current_sample.content
    else:
        text_for_comparison = None
    current_sample = None
    callback(0)