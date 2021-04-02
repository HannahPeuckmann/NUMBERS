# rule based nlu

import re
from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU
from retico.core.dialogue.common import DialogueActIU


class NLUModule(abstract.AbstractModule):
    @staticmethod
    def name():
        return "NLU module"

    @staticmethod
    def description():
        return (
            """NLU based on rules."""
        )

    @staticmethod
    def input_ius():
        return [SpeechRecognitionIU]

    @staticmethod
    def output_iu():
        return DialogueActIU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lb_hypotheses = []
    def get_current_text(self, input_iu):
        self.lb_hypotheses.append(input_iu.get_text())
        txt = ""
        for iu in self.lb_hypotheses:
            txt += iu
        return txt

    ## pattern matcher nach aho und corasic als transduktor maybe?
    def _parse(self, text):
        intents_values = [("transmit","\d+"),\
                          ("yes","ja|richtig|das ist richtig|genau|ja, richtig"),\
                          ("no","nein|ne|falsch|Fehler"),\
                          ]
        intent_value = {"intent": None, "value":None}
        for i, v in intents_values:
            v = re.findall(v, text)
            if v != []:
                intent_value["intent"] = i
                if i == "transmit":
                    intent_value["value"] = v
                break
        if intent_value["intent"] == None:
            return None
        return intent_value

    def process_iu(self, input_iu):
        if input_iu.eot == True:
            output_iu = self.create_iu()
            output_iu.eot = True
            self.lb_hypotheses = []
            return output_iu
        if input_iu.mot == True:
            output_iu =self.create_iu()
            output_iu.mot = True
            return output_iu

        current_text = input_iu.get_text()
        if not current_text:
            return None
        result = self._parse(current_text)
        if result:
            output_iu = self.create_iu(input_iu)
            output_iu.set_act(result["intent"], result["value"], 100) 
            print(output_iu.act)
            piu = output_iu.previous_iu
            if piu:
                if piu.act != output_iu.act or piu.concepts != output_iu.concepts:
                    piu.revoked = True
            self.append(output_iu)



