from datetime import datetime

class Sample():
    def __init__(self, content, inputtime, username, values_per_feature_and_char):
        self.content = content
        self.inputtime = inputtime
        self.username = username
        self.values_per_feature_and_char = values_per_feature_and_char

    def get_formatted_inputtime(self):
        return datetime.fromtimestamp(self.inputtime/1000.0).strftime("%d.%m.%Y, %H:%M:%S")

    def get_short_identifier(self):
        maxlength = 60
        identifier = self.username + " (" + self.get_formatted_inputtime() + ") "
        maxlength -= len(identifier)
        identifier += self.content[:maxlength] + "..."
        return identifier

    # textfield for displaying entered text
    def get_content_and_values_overview(self):
        if self.values_per_feature_and_char:    
            return self.content + "\n\n\nRecorded values in ms: " + str(self.values_per_feature_and_char)
        return "No values recorded."

    def create_file_name(self):
        # random letters to make filename unique and prevent unusual case: two user with same username entered text on same time (f.e. on different devices)
        return self.username + str(self.inputtime) + ".txt"