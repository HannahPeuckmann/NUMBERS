# silence detection

from retico_builder.modules.abstract import AbstractModule
from retico.own_modules.eot import EOTModule


class EOTModule(AbstractModule):

    MODULE = EOTModule

    def set_content(self):
        self.gui.clear_content()


