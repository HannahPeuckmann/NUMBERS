# dialogue manager

import logging
from retico.core import abstract
from retico.core.text.common import GeneratedTextIU
from retico.core.dialogue.common import DialogueActIU

#### ask for confirmation if asr_confidence is low in the next episode of detected silence

class DM(abstract.AbstractModule):
    """A customized dialogue manager."""

    @staticmethod
    def name():
        return "Dialogue Manager Module"

    @staticmethod
    def description():
        return "A Module that decides which action to take"

    @staticmethod
    def input_ius():
        return [DialogueActIU]

    @staticmethod
    def output_iu():
        return GeneratedTextIU

    def __init__(self, **kwargs):
        """Initialise the dialogue manager."""
        super().__init__(**kwargs)
        self.final_numbers = []
        self.numbers = []
        self.intent = None
        self.entitys = None
        logging.basicConfig(level=logging.DEBUG, filename="NUMBERS.log")
        self.user_iu_counter = 0
        self.mot = False

    def _get_intent_entities(self, input_iu):
        self.intent = input_iu.act
        self.values = input_iu.concepts

    def process_iu(self, input_iu):
        if abstract.AbstractModule.LISTENING:
            if input_iu.eot == True and self.user_iu_counter > 0:
                self._confirm_handler()
                self.mot = False
                return
            if abstract.AbstractModule.CONFIRMING == False and input_iu.mot == True and self.user_iu_counter > 0:
                self.mot = True
                self._create_iu("ja?")
            self._get_intent_entities(input_iu)
            self.user_iu_counter += 1
            if self.intent == "yes":
                self._create_iu("cool, machs gut.")
                return 
            if self.intent == 'transmit':
                self._transmit_handler()


    def _transmit_handler(self, asr_confidence=100):
        flatten = lambda superior_list: [number for sublist in superior_list for number in sublist]
        self.numbers = [Number(num, asr_confidence) for num in flatten(self.values)]
        if self.mot:
            self.final_numbers.extend(self.numbers)

    def _confirm_handler(self):
        if abstract.AbstractModule.LISTENING and abstract.AbstractModule.CONFIRMING == False:
                abstract.AbstractModule.CONFIRMING = True
                values = ", "
                values = values.join([num.value for num in self.final_numbers])
                print(values)
                self._create_iu(f"Ok, die Zahlen sind: {values}, ist das richtig?")
                self.user_iu_counter = 0


    def _error_handler(self):
        self.numbers = []
        self._create_iu('Das tut mir leid, bitte sag mir die Zahlen noch ein mal')
        print('Das tut mir leid, bitte sag mir die Zahlen noch ein mal')
        self.user_iu_counter = 0

    def _create_iu(self, text):
        output_iu = self.create_iu()
        output_iu.set_text(text)
        self.append(output_iu)

    def setup_dm(self):
        self._create_iu('Hi, bitte diktiere mir die Zahlen, die du vor dir siehst,\n\
                als würdest du sie am telefon durchgeben.\n\
                Um das Programm zu beenden, drücke ENTER.\n\
                Für Hilfe, frage einfach nach Hilfe.')

class Number:
    def __init__(self, value, confidence):
        self.confirmed = False
        self.confidence = confidence
        self.value = value
    
    def __str__(self) -> str:
        return self.value

