import controller.keyboardcapture as k
import unittest

class TestKeyboardcapture(unittest.TestCase):
    all_keyboard_actions_for_test = [
        # tuple with milliseconds, character and eventtype as number (2=down, 3=up)
        (2, 'a', 2),
        (200, 'a', 3),
        (400, 'b', 2),
        (600, 'c', 2),
        (800, 'b', 3),
        (1500, 'c', 3)        
    ]

    def test_find_next_down_and_up_time(self):
        # char, all_keyboard_actions
        return

    def test_find_next_down_and_up_time_non_existent_down(self):
        # char, all_keyboard_actions
        return

    def test_find_next_down_and_up_time_non_existent_up(self):
        # char, all_keyboard_actions
        return

    def test_create_value_entry(self):
        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_minuend_none(self):
        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_subtrahend_none(self):
        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_duplicate_key(self):
        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_extract_values_per_feature_and_chars(self):
        # create text, all_keyboard_actions
        return

    def test_stop_recording(self):
        # fill all_keyboard_actions
        return

if __name__ == '__main__':
    unittest.main()
