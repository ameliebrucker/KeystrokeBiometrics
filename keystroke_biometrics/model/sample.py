from datetime import datetime

class Sample():
    """
    A class for representing a sample of a user input with keystrokes
    
    Attributes (Object)
    content: string, total text entered
    inputtime: int, time of first keyboard input from sample in milliseconds
    username: string, name/alias of user
    values_per_feature_and_chars: dictionary with pairs of feature and chars (key) and all belonging time values (value)

    Methods
    get_short_identifier(): gives an identifier of the sample containing username, formatted inputtime and short content
    get_content_and_values_overview(): gives a formatted summary of content and values per features and chars
    get_file_name(): gives a file name for the sample containing username and inputtime in milliseconds
    """

    def __init__(self, content, inputtime, username, values_per_feature_and_chars):
        self.content = content
        self.inputtime = inputtime
        self.username = username
        self.values_per_feature_and_chars = values_per_feature_and_chars

    def get_short_identifier(self):
        """
        gives an identifier of the sample containing username, formatted inputtime and short content

        Return:
        identifier as string

        Precondition:
        content, inputtime and username are initialized
        """

        maxlength = 60
        # create time in format dd.mm.yyyy, hh:mm:ss
        formatted_inputtime = datetime.fromtimestamp(self.inputtime/1000.0).strftime("%d.%m.%Y, %H:%M:%S")
        identifier = f"{self.username} ({formatted_inputtime}) "
        maxlength -= len(identifier)
        if len(self.content) > maxlength:
            identifier += f"{self.content[:maxlength - 3]}..."
        else:
            identifier += self.content
        return identifier

    def get_content_and_values_overview(self):
        """
        gives a formatted summary of content and values per features and chars

        Return:
        content and values per features and chars as string

        Precondition:
        content and values_per_feature_and_chars are initialized
        """

        return f"{self.content}\n\n\nRecorded values in ms: {self.values_per_feature_and_chars}"    
        

    def get_file_name(self):
        """
        gives a file name for the sample containing username and inputtime in milliseconds

        Return:
        filename as string

        Precondition:
        username and inputtime are initialized
        """

        return f"{self.username}{self.inputtime}.txt"