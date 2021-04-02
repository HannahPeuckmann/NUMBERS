from gtts import gTTS

audio = gTTS("hallo bitte diktiere mir die Zahlen", lang='de')
audio.save('ttsfile.mp3')