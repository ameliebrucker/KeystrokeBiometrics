from datetime import *

class Sample():
    def __init__(self, content, inputtime, username, values_per_feature_and_char):
        self.content = content
        self.inputtime = inputtime
        self.username = username
        self.values_per_feature_and_char = values_per_feature_and_char
        # textfield for displaying entered text
    def get_short_identifier(self):
        maxlength = 60
        identifier = self.username + " (" + self.inputtime + ") "
        maxlength -= len(identifier)
        identifier += self.content[:maxlength] + "..."
        return identifier
    def get_text_and_value_overview(self):
        return self.content + "\n\n\nRecorded values: " + str(self.values_per_feature_and_char)