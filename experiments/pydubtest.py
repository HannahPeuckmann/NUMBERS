from pydub import AudioSegment
from pydub.silence import detect_silence

audio = AudioSegment.from_wav('speaking.wav')
print(audio.__len__())
silence = detect_silence(audio, 10, -16)
print(silence)

