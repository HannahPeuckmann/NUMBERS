
from retico.own_modules.feedback import TextOutputModule
from retico.core.audio.io import MicrophoneModule
from retico.modules.google.asr import GoogleASRModule




mic = MicrophoneModule(5000)
asr = GoogleASRModule(language='de-DE')
out = TextOutputModule()

mic.subscribe(asr)
asr.subscribe(out)

mic.run()
asr.run()
out.run()


print("startet and running")

input()

print("exiting")

mic.stop()
asr.stop()
out.stop()

