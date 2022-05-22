import controller.keyboardcapture as k
from model.feature import Feature
import unittest

class TestKeyboardcapture(unittest.TestCase):
    """
    A class for testing functions from keyboardcapture module

    Attributes (Object)
    keyboard_actions_for_testing: example keyboard_actions list for test functions

    Methods
    setUp(): sets up test values for tests
    test_find_next_down_and_up(): tests the find_next_down_and_up() function
    test_find_next_down_and_up_non_existent_down(): tests the find_next_down_and_up() function with non existent down value
    test_find_next_down_and_up_non_existent_up(): tests the find_next_down_and_up() function with non existent up value
    test_create_value_entry(): tests the create_value_entry() function
    test_create_value_entry_minuend_none(): tests the create_value_entry() function with None as minuend
    test_create_value_entry_subtrahend_none(): tests the create_value_entry() function with None as subtrahend
    test_create_value_entry_duplicate_key(): tests the create_value_entry() function for an existing key
    test_extract_values_per_feature_and_chars(): tests the extract_values_per_feature_and_chars() function
    test_stop_recording(): tests the stop_recording() function
    """


    def setUp(self):
        """
        sets up test values for tests
        """

        k.all_keyboard_actions = [
        # tuple with milliseconds, character and eventtype as number (2=down, 3=up)
        (100, 'a', '2'),
        (200, 'a', '3'),
        (400, 'b', '2'),
        (600, 'c', '2'),
        (800, 'b', '3'),
        (2000, 'd', '3')
        ]

    def test_find_next_down_and_up(self):
        """
        tests the find_next_down_and_up() function from keyboardcapture module
        """

        ref_result = ((100, 'a', '2'), (200, 'a', '3'))
        ref_all_keyboardactions = [
            (400, 'b', '2'),
            (600, 'c', '2'),
            (800, 'b', '3'),
            (2000, 'd', '3')
        ]
        self.assertEqual(k.find_next_down_and_up('a'), ref_result)
        self.assertEqual(k.all_keyboard_actions, ref_all_keyboardactions)

    def test_find_next_down_and_up_non_existent_down(self):
        """
        tests the find_next_down_and_up() function from keyboardcapture module with non existent down value
        """

        ref_result = (None, (2000, 'd', '3'))
        ref_all_keyboardactions = [
            (100, 'a', '2'),
            (200, 'a', '3'),
            (400, 'b', '2'),
            (600, 'c', '2'),
            (800, 'b', '3')
        ]
        self.assertEqual(k.find_next_down_and_up('d'), ref_result)
        self.assertEqual(k.all_keyboard_actions, ref_all_keyboardactions)

    def test_find_next_down_and_up_non_existent_up(self):
        """
        tests the find_next_down_and_up() function from keyboardcapture module with non existent up value
        """

        ref_result = ((600, 'c', '2'), None)
        ref_all_keyboardactions = [
            (100, 'a', '2'),
            (200, 'a', '3'),
            (400, 'b', '2'),
            (800, 'b', '3'),
            (2000, 'd', '3')
        ]
        self.assertEqual(k.find_next_down_and_up('c'), ref_result)
        self.assertEqual(k.all_keyboard_actions, ref_all_keyboardactions)

    def test_create_value_entry(self):
        """
        tests the create_value_entry() function from keyboardcapture module
        """

        dict = {}
        k.create_value_entry(Feature.M, k.all_keyboard_actions[1], k.all_keyboard_actions[0], 'a', dict)
        self.assertEqual(dict, {(Feature.M.value, 'a') : [100]})

    def test_create_value_entry_minuend_none(self):
        """
        tests the create_value_entry() function from keyboardcapture module with None as minuend
        """

        dict = {}
        k.create_value_entry(Feature.M, None, k.all_keyboard_actions[0], 'a', dict)
        self.assertEqual(dict, {})

    def test_create_value_entry_subtrahend_none(self):
        """
        tests the create_value_entry() function from keyboardcapture module with None as subtrahend
        """

        dict = {}
        k.create_value_entry(Feature.M, k.all_keyboard_actions[1], None, 'a', dict)
        self.assertEqual(dict, {})

    def test_create_value_entry_duplicate_key(self):
        """
        tests the create_value_entry() function from keyboardcapture module for an existing key
        """

        dict = {(Feature.M.value, 'a') : [200]}
        k.create_value_entry(Feature.M, k.all_keyboard_actions[1], k.all_keyboard_actions[0], 'a', dict)
        self.assertEqual(dict, {(Feature.M.value, 'a') : [200, 100]})

    def test_extract_values_per_feature_and_chars(self):
        """
        tests the extract_values_per_feature_and_chars() function from keyboardcapture module
        """

        ref = ({
            (Feature.M.value, 'a') : [100],
            (Feature.M.value, 'b') : [400],
            (Feature.DD.value, 'ab') : [300],
            (Feature.UD.value, 'ab') : [200],
            (Feature.DU.value, 'ab') : [700],
            (Feature.UU.value, 'ab') : [600],
        }, 100)
        self.assertEqual(k.extract_values_per_feature_and_chars("ab"), ref)
        self.assertEqual(k.all_keyboard_actions, [])

    def test_stop_recording(self):
        """
        tests the stop_recording() function from keyboardcapture module
        """

        k.stop_recording()
        self.assertEqual(k.all_keyboard_actions, [])

if __name__ == '__main__':
    unittest.main()
