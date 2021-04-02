# rule based nlu

from retico_builder.modules.abstract import AbstractModule
from retico.own_modules.nlu import NLUModule


class NLUModule(AbstractModule):
    
    MODULE = NLUModule

    def set_content(self):
        self.gui.clear_content()




