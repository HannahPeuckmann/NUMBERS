"""
This module handles input and output of text to the shell.
"""

from retico.core.abstract import AbstractConsumingModule
from retico.core.text.common import TextIU, GeneratedTextIU, SpeechRecognitionIU



class TextOutputModule(AbstractConsumingModule):
    """A module that writes the received text to the shell."""

    @staticmethod
    def name():
        return "Text Output Module"

    @staticmethod
    def description():
        return "A module that writes received TextIUs to the shell"

    @staticmethod
    def input_ius():
        return [TextIU, GeneratedTextIU, SpeechRecognitionIU]

    def __init__(self, separator="\n", **kwargs):
        super().__init__(**kwargs)
        self.separator = separator
        self.txt_file = None

    def process_iu(self, input_iu):
        print("in process")
        print(input_iu.get_text())
        if isinstance(input_iu, GeneratedTextIU):
            print(self.separator)
            print(str(input_iu.dispatch))
        if isinstance(input_iu, SpeechRecognitionIU):
            print(str(input_iu.final))
