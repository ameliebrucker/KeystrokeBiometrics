import time
from feature import Feature

# list of tuples with time in milliseconds, character and eventtype as number (2=down, 3=up) for every keystroke event
all_keyboard_actions = []

def record_keyboard_entries(event):
    """
    saves time in milliseconds, character and eventtype as number (2=down, 3=up) from keystroke event to list all_keyboard_actions as tuple

    Parameter:
    event: keystroke event from typing in text field

    Precondition:
    list all_keyboard_actions has been initialized
    """

    all_keyboard_actions.append((round(time.time()*1000), event.char, event.type))        

def stop_recording():
    """
    resets all_keyboard_actions in order to terminate current recording
    """

    global all_keyboard_actions
    all_keyboard_actions = []

def extract_values_per_feature_and_chars(text):
    """
    creates dictionary with calcuated time values grouped by feature and chars, terminates current recording

    Parameter:
    text: full text entered into input field during current recording

    Return:
    result: dictionary with pairs of feature and chars (key) and all belonging time values (value)
    inputtime: time of first keystroke event during current recording

    Precondition:
    list all_keyboard_actions has been initialized
    """

    # set inputtime based on first measured time value
    inputtime = all_keyboard_actions[0][0]
    result = {}
    previous_char = None
    # for every char in text, determine time values for all recognizable features
    for current_char in text:
        # get up and down time for char
        current_char_down, current_char_up = find_next_down_and_up_time(current_char)
        # determine monograph feature
        create_value_entry(Feature.M, current_char_up, current_char_down, current_char, result)
        if (previous_char is not None):
            # determine digraph features
            chars = previous_char + current_char
            create_value_entry(Feature.DD, current_char_down, previous_char_down, chars, result)
            create_value_entry(Feature.UD, current_char_down, previous_char_up, chars, result)
            create_value_entry(Feature.DU, current_char_up, previous_char_down, chars, result)
            create_value_entry(Feature.UU, current_char_up, previous_char_up, chars, result)    
        previous_char = current_char
        previous_char_down, previous_char_up = current_char_down, current_char_up
    # remove old data in case there are unusual records which were not cleaned in find_next_down_and_up_time()
    stop_recording()
    return result, inputtime

def find_next_down_and_up_time(char):
    """
    finds next tuple for key press and release for given char, returns time and deletes tuple from all_keyboard_actions

    Parameter:
    char: char for which tuples should be found

    Return:
    down: time which belongs to next key press for char
    up: time which belongs to next key release for char

    Precondition:
    list all_keyboard_actions has been initialized
    """

    # find tuple with given char and eventtype 2 (key press event) / 3 (key release event)
    # lower char to avoid unmatching pairs if shift key is released during pressing char key
    down = next(filter(lambda d: d[1].lower() == char.lower() and d[2] == '2', all_keyboard_actions), None)
    up = next(filter(lambda d: d[1].lower() == char.lower() and d[2] == '3', all_keyboard_actions), None)
    # delete processed data to put next tuples always in front
    if down is not None:
        all_keyboard_actions.remove(down)
    if up is not None:
        all_keyboard_actions.remove(up)
    return down[0], up[0]

def create_value_entry (featurename, minuend, subtrahend, chars, values_per_feature_and_chars):
    """
    calculates time span and inserts entry to dictionary according to pattern: key (featurename, chars) : value [timespan_1, ..., timespan_n]

    Parameter:
    featurename: name of the currently observed feature
    minuend: minuend in subtraction for time calculation
    subtrahend: subtrahend in subtraction for time calculation
    chars: currently observed chars
    values_per_feature_and_chars: dictionary in which entries should be inserted
    """

    if minuend is not None and subtrahend is not None:
        result = minuend - subtrahend
        if (featurename.value, chars) in values_per_feature_and_chars:
            # key is already included in dictionary
            values_per_feature_and_chars[(featurename.value, chars)].append(result)
        else:
            values_per_feature_and_chars[(featurename.value, chars)] = [result]
