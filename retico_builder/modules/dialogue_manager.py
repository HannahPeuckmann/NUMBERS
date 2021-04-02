# dialogue manager


from flexx import flx
from retico_builder.modules.abstract import AbstractModule
from retico.own_modules.dialogue_manager import DM

#### ask for confirmation if asr_confidence is low in the next episode of detected silence

class DM(AbstractModule):
    """A customized dialogue manager."""
    MODULE = DM
    PARAMS = {}

    def set_content(self):
        self.gui.clear_content()

