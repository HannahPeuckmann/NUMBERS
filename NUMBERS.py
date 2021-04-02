# NUMBERS, incremental numbers dictating dialogue system.

# reimplementation of the NUMBERS system by Schlangen and Skantze(200..)
# by making use of the existing Framework ReTiCo by Baumann and ....
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
mot = MOTModule(0.5)
#eot = EOTModule(1.2)
asr = GoogleASRModule(language='de-DE')
nlu = NLUModule()
dm = DM()
tts = GoogleTTSModule("de_DE", "de-DE-Wavenet-C")
speaker = SpeakerModule()

mic.subscribe(asr)
#asr.subscribe(eot)
asr.subscribe(mot)
asr.subscribe(nlu)
mot.subscribe(dm)
#eot.subscribe(dm)
nlu.subscribe(dm)
dm.subscribe(tts)
tts.subscribe(speaker)

mic.run()
asr.run()
mot.run()
#eot.run()
nlu.run()
dm.run()
tts.run()
speaker.run()

print("startet and running")

dm.setup_dm()

input()

print("exiting")

mic.stop()
mot.stop()
asr.stop()
#eot.stop()
nlu.stop()
dm.stop()
tts.stop()
speaker.stop()
