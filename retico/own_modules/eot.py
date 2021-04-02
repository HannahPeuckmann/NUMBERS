# silence detection
import threading
import sched, time
from retico.core import abstract
from retico.core.audio.common import AudioIU
from retico.core.text.common import SpeechRecognitionIU
from retico.core.dialogue.common import DialogueActIU

class EOTModule(abstract.AbstractModule):

    silence_detected_event = None
    should_send_silence = False

    @staticmethod
    def name():
        return "End of turn"

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
        return DialogueActIU

    def __init__(self, eot_threshold=8.0, **kwargs):
        super().__init__(**kwargs)
        self.eot = False
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.eot_silence_threshold = eot_threshold # in seconds
        t = threading.Thread(target=self.send_silence_detected_after_delay)
        t.start()

    def process_iu(self, input_iu):
        self.remove_silence_detection_event()
        EOTModule.should_send_silence = True

    def remove_silence_detection_event(self):
        list(map(self.scheduler.cancel, self.scheduler.queue))

    def send_silence_detected(self):
        self.eot = True
        output_iu = self.create_iu()
        output_iu.eot = True
        print("send eot")
        self.append(output_iu)

    def send_silence_detected_after_delay(self):
        while True:
            if EOTModule.should_send_silence:
                self.scheduler.enter(self.eot_silence_threshold, 1, self.send_silence_detected)
                self.scheduler.run()
                EOTModule.should_send_silence = False
