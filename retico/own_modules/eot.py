# silence detection

import logging
from retico.core import abstract
from retico.core.audio.common import AudioIU
from retico.core.text.common import SpeechRecognitionIU


class EOTModule(abstract.AbstractModule):
    @staticmethod
    def name():
        return "End of turn module"

    @staticmethod
    def description():
        return (
            """A module that sends an end of turn signal trough the modules
            if it is not receiving any ius from the asr for a set timeframe."""
        )

    @staticmethod
    def input_ius():
        return [AudioIU, SpeechRecognitionIU]

    @staticmethod
    def output_iu():
        return SpeechRecognitionIU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.seconds = 0
        #1.5 sec of no asr input signals eot for now
        self.eot_silence_thrashold = 1.5
        self.eot = False
        self.mot_silence_thrashold = 0.7
        self.mot = False
        logging.basicConfig(level=logging.DEBUG, filename="NUMBERS.log")

    def process_iu(self, input_iu):
        if input_iu.type() == "Audio IU":
            self.seconds += input_iu.audio_length()
            if not self.mot and self.seconds > self.mot_silence_thrashold and self.iu_counter > 0:
                print("mot detected")
                self.mot = True
                logging.debug("from eot: mot detected")
                output_iu = self.create_iu()
                output_iu.mot = True
                self.append(output_iu)
            if not self.eot and self.seconds > self.eot_silence_thrashold and self.iu_counter > 0:
                self.seconds = 0
                print("eot detected")
                self.eot = True
                logging.debug("from eot: eot detected")
                output_iu = self.create_iu()
                output_iu.eot = True
                self.append(output_iu)
                return
        else:
            if abstract.AbstractModule.LISTENING:
                self.seconds = 0
                self.iu_counter += 1
                if self.eot == True:
                    print("set eot to false")
                self.eot = False
                self.append(input_iu)


