# silence detection
import logging
import threading
import sched, time
from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU

logging.basicConfig(filename='numbers.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

class MOTModule(abstract.AbstractModule):
    silence_detected_event = None
    should_send_silence = False

    @staticmethod
    def name():
        return "Mid turn break"

    @staticmethod
    def description():
        return (
            """A module that sends an end of turn signal trough the modules
            if it is not receiving any ius from the asr for a set timeframe."""
        )

    @staticmethod
    def input_ius():
        return [SpeechRecognitionIU]

    @staticmethod
    def output_iu():
        return SpeechRecognitionIU

    def __init__(self, mot_threshold=0.3, **kwargs):
        super().__init__(**kwargs)
        self.mot = False
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.mot_silence_threshold = mot_threshold # in seconds
        t = threading.Thread(target=self.send_silence_detected_after_delay)
        t.start()

    def process_iu(self, input_iu):
        self.remove_silence_detection_event()
        self.append(input_iu)
        MOTModule.should_send_silence = True

    def remove_silence_detection_event(self):
        list(map(self.scheduler.cancel, self.scheduler.queue))

    def send_silence_detected(self):
        self.mot = True
        output_iu = self.create_iu()
        output_iu.mot = True
        logging.debug("mot send")
        self.append(output_iu)

    def send_silence_detected_after_delay(self):
        while True:
            if MOTModule.should_send_silence:
                self.scheduler.enter(self.mot_silence_threshold, 1, self.send_silence_detected)
                self.scheduler.run()
                MOTModule.should_send_silence = False
