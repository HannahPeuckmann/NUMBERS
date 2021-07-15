# NUMBERS, incremental dialogue system in the number dictation domain.

# reimplementation of the NUMBERS system by Schlangen and Skantze
# by making use of the existing framework ReTiCo by Baumann and Michael
# for building incemental dilogue systems

from retico.own_modules.eot import EOTModule
from retico.own_modules.mot import MOTModule
from retico.own_modules.dialogue_manager import DM
from retico.core.audio.io import MicrophoneModule, SpeakerModule
from retico.core.text.asr import IncrementalizeASRModule
from retico.modules.google.asr import GoogleASRModule
from retico.modules.google.tts import GoogleTTSModule
from retico.own_modules.nlu import NLUModule




mic = MicrophoneModule(5000)
mot = MOTModule()
eot = EOTModule()
asr = GoogleASRModule(language='de-DE')
nlu = NLUModule()
dm = DM()
tts = GoogleTTSModule("de_DE", "de-DE-Wavenet-C")
speaker = SpeakerModule()

mic.subscribe(asr)
asr.subscribe(eot)
asr.subscribe(mot)
asr.subscribe(nlu)
mot.subscribe(dm)
eot.subscribe(dm)
nlu.subscribe(dm)
dm.subscribe(tts)
tts.subscribe(speaker)

mic.run()
asr.run()
mot.run()
eot.run()
nlu.run()
dm.run()
tts.run()
speaker.run()

print("startet and running")

dm.setup_dm()

input()

print("exiting")

mic.stop()
asr.stop()
mot.stop()
eot.stop()
nlu.stop()
dm.stop()
tts.stop()
speaker.stop()
