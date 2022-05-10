import keyboardcapture

from sample import Sample

text_for_comparison = None
current_username = "Anonym"
current_sample = None

# keyboard recording

def form_sample_from_entry(event, callback = None, username="Anonym", text = ""):
    if callback is not None:
        # return key was pressed, keyboard recognition is over
        values_for_sample = keyboardcapture.extract_values_per_feature_and_chars(text)
        inputtime = keyboardcapture.inputtime
        keyboardcapture.stop_recording()
        global current_sample
        global current_username
        current_username = username
        current_sample = Sample(text, inputtime, current_username, values_for_sample)
        callback (2, current_sample.get_text_and_value_overview())
    else:
        keyboardcapture.record_keyboard_entries(event)

def get_all_sample_identifier():
    if current_sample is not None:
        return("Username41", current_sample.get_short_identifier())
    else:
        return("Username41",)