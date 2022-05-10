import time
from datetime import datetime
#from tkinter import EventType
import Feature

all_keyboard_actions = []
values_per_feature_and_chars = {}
inputtime = None
#down_event_type = <EventType.KeyPress: '2'>

def record_keyboard_entries(event):
    # add time in ms, char and eventtype in number (2=down, 3=up)
    all_keyboard_actions.append((round(time.time()*1000), event.char, event.type))
    global inputtime
    if inputtime is None:
        inputtime = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")

def stop_recording():
    #all keyboard_actions should already be cleaned in extract values func if its working properly
    global all_keyboard_actions
    global values_per_feature_and_chars
    global inputtime
    all_keyboard_actions = []
    values_per_feature_and_chars = {}
    inputtime = 0

# extracts values bla bla and stops recording
def extract_values_per_feature_and_chars(text):
    previous_char = None
    for current_char in text:
        current_char_down, current_char_up = find_up_and_down_time(current_char)
        create_value_entry(Feature.monograph, current_char_up, current_char_down, current_char)

        if (previous_char is not None):
            chars = previous_char + current_char
            create_value_entry(Feature.down_down, current_char_down, previous_char_down, chars)
            create_value_entry(Feature.up_down, current_char_down, previous_char_up, chars)
            create_value_entry(Feature.down_up, current_char_up, previous_char_down, chars)
            create_value_entry(Feature.up_up, current_char_up, previous_char_up, chars)

        previous_char = current_char
        previous_char_down, previous_char_up = current_char_down, current_char_up
    return values_per_feature_and_chars

def find_up_and_down_time(char):
    # find value with down: <EventType.KeyPress: '2'> and char ?
    down = next(filter(lambda d: d[1] == char and d[2] == '2', all_keyboard_actions), None)
    up = next(filter(lambda d: d[1] == char and d[2] == '3', all_keyboard_actions), None)
    # evtl. prüfen ob index von up nach down, um fehler auszuschließen, aber einziger anwendungsfall wäre wenn jmd mit gedrückter taste feld öffnet
    if down is not None:
        all_keyboard_actions.remove(down)
    if up is not None:
        all_keyboard_actions.remove(up)
    return down, up

def create_value_entry (featurename, minuend, subtrahend, chars):
    if minuend is not None and subtrahend is not None:
        result = minuend[0] - subtrahend[0]
        values_per_feature_and_chars[chars + "-" + featurename] = result
