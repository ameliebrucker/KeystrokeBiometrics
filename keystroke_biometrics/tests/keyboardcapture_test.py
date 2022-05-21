import controller.keyboardcapture as k
import unittest

class TestKeyboardcapture(unittest.TestCase):
    """
    A class for testing functions from keyboardcapture module

    Attributes (Object)
    keyboard_actions_for_testing: example keyboard_actions list for test functions

    Methods
    setUp(): sets up test values for tests
    test_find_next_down_and_up_time(): tests the find_next_down_and_up_time() function
    test_find_next_down_and_up_time_non_existent_down(): tests the find_next_down_and_up_time() function with non existent down value
    test_find_next_down_and_up_time_non_existent_up(): tests the find_next_down_and_up_time() function with non existent up value
    test_create_value_entry(): tests the create_value_entry() function
    test_create_value_entry_minuend_none(): tests the create_value_entry() function with None as minuend
    test_create_value_entry_subtrahend_none(): tests the create_value_entry() function with None as subtrahend
    test_create_value_entry_duplicate_key(): tests the create_value_entry() function for an existing key
    test_extract_values_per_feature_and_chars(): tests the extract_values_per_feature_and_chars() function
    """


    def setUp(self):
        """
        sets up test values for tests
        """

        self.keyboard_actions_for_testing = [
        # tuple with milliseconds, character and eventtype as number (2=down, 3=up)
        (2, 'a', 2),
        (200, 'a', 3),
        (400, 'b', 2),
        (600, 'c', 2),
        (800, 'b', 3),
        (1500, 'c', 3)        
        ]

    def test_find_next_down_and_up_time(self):
        """
        tests the find_next_down_and_up_time() function from keyboardcapture module
        """

        # char, all_keyboard_actions
        return

    def test_find_next_down_and_up_time_non_existent_down(self):
        """
        tests the find_next_down_and_up_time() function from keyboardcapture module with non existent down value
        """

        # char, all_keyboard_actions
        return

    def test_find_next_down_and_up_time_non_existent_up(self):
        """
        tests the find_next_down_and_up_time() function from keyboardcapture module with non existent up value
        """

        # char, all_keyboard_actions
        return

    def test_create_value_entry(self):
        """
        tests the create_value_entry() function from keyboardcapture module
        """

        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_minuend_none(self):
        """
        tests the create_value_entry() function from keyboardcapture module with None as minuend
        """

        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_subtrahend_none(self):
        """
        tests the create_value_entry() function from keyboardcapture module with None as subtrahend
        """

        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_create_value_entry_duplicate_key(self):
        """
        tests the create_value_entry() function from keyboardcapture module for an existing key
        """

        # create featurename, minuend, subtrahend, chars, values_per_feature_and_chars
        return

    def test_extract_values_per_feature_and_chars(self):
        """
        tests the extract_values_per_feature_and_chars() function from keyboardcapture module
        """

        # create text, all_keyboard_actions
        return

if __name__ == '__main__':
    unittest.main()
