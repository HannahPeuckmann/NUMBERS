# silence detection

from retico_builder.modules.abstract import AbstractModule
from retico.own_modules.mot import MOTModule


class MOTModule(AbstractModule):
    
    MODULE = MOTModule

    def set_content(self):
        self.gui.clear_content()


