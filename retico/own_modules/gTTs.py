
from retico.core import abstract
from retico.core.text.common import GeneratedTextIU
from retico.core.audio.common import SpeechIU
from google.cloud import texttospeech

"""
A module that uses Google TTS to create speech from text.
"""

import os
import subprocess
import random
import wave
from hashlib import blake2b

from retico.core import abstract, text, audio

# Helper functions ==============


class GoogleTTS:
    """
    A google TTS class that is able to return the audio as pcm.

    This class relies on gcloud and ffmpeg to be installed and available.
    """

    CACHING_DIR = "data_tts/gtts_cache/"
    TEMP_DIR = "/tmp"
    TEMP_NAME = "tmp_tts_%s" % random.randint(1000,10000)

    def __init__(self, caching=True):
        """
        Creates a Google TTS instance with the specified language_code and voice_name.
        The valid values can be looked up [here](https://cloud.google.com/text-to-speech/docs/voices).

        Args:
            language_code (str): The language code specified by google cloud (e.g. en-US or de-DE)
            voice_name (str): The name of the voice specified by google cloude
            caching (bool): Whether the tts should cache the speech.
        """
        self.caching = caching

        self.wav_sample_rate = 44100 # 44100 sample rate / See ffmpeg
        self.wav_codec = "pcm_s16le" # 16-bit little endian codec / See ffmpeg

        client = texttospeech.TextToSpeechClient()

        # Create caching directory if it not already exists
        if not os.path.exists(self.CACHING_DIR):
            os.mkdir(self.CACHING_DIR)

    def get_cache_path(self, text):
        """
        Creates a hash of the given TTS settings and returns a unique path to the cached version of the synthesis.
        This method does not check for the cached file to exist!

        Args:
            text (str): The text to synthesis (this is included in the hash that is used for the cache path)

        Returns (str): Path to a cached version of that synthesis.

        """
        h = blake2b(digest_size=16)
        h.update(bytes(text, 'utf-8'))
        h.update(bytes(self.language_code, 'utf-8'))
        h.update(bytes(self.wav_codec, 'utf-8'))
        h.update(bytes(str(self.wav_sample_rate), 'utf-8')) # Wait this makes no sense. FIXME
        h.update(bytes(str(self.speaking_rate), 'utf-8'))  # Wait this makes no sense. FIXME
        text_digest = h.hexdigest()

        return os.path.join(self.CACHING_DIR, text_digest)

    def tts(self, text):
        """
        Synthesizes the text given and returns it in PCM format. This method uses the wave_sample_rate and wave_codec
        properties to determine the shape of the synthesized audio.
        The returned audio does not have any wave header but contains jus the pure PCM data.

        Args:
            text (str): The text to synthesize

        Returns (bytes): The synthesized text in raw PCM format.
        """
        cache_path = self.get_cache_path(text)
        if os.path.isfile(cache_path):
            wav_audio = None
            with open(cache_path, 'rb') as cfile:
                wav_audio = cfile.read()
        else:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="de-DE", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            wav_audio = self.convert_audio(response)
            with open(cache_path, 'wb') as cfile:
                cfile.write(wav_audio)


        return wav_audio

    def convert_audio(self, audio):
        """
        Converts the given mp3 audio to the respecitve pcm data through ffmpeg.
        This function assumes ffmpeg is installed and readily available.

        Args:
            audio (bytes): The mp3 audio data as given by Google TTS

        Returns (bytes): The pcm data as specified by wav_codec and wav_sample_rate. Note that this byte array does not
            contain the wave header (or any other header) but is just the raw audio data.

        """
        tmp_mp3_name = self.TEMP_NAME + ".mp3"
        tmp_wav_name = self.TEMP_NAME + ".wav"
        tmp_mp3_path = os.path.join(self.TEMP_DIR, tmp_mp3_name)
        tmp_wav_path = os.path.join(self.TEMP_DIR, tmp_wav_name)

        # The response's audio_content is binary.
        with open(tmp_mp3_name, "wb") as out:
            # Write the response to the output file.
            out.write(audio.audio_content)

        subprocess.call(["ffmpeg", "-i", tmp_mp3_path, "-acodec", self.wav_codec, "-ar", str(self.wav_sample_rate), tmp_wav_path, "-y"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

        wav_audio = None
        with wave.open(tmp_wav_path, 'rb') as wav_file:
            w_length = wav_file.getnframes()
            wav_audio = wav_file.readframes(w_length)

        # Cleanup
        os.remove(tmp_mp3_path)
        os.remove(tmp_wav_path)

        return wav_audio

class GoogleTTSModule(abstract.AbstractModule):
    """A Google TTS Module that uses Googles TTS service to synthesize audio."""
    @staticmethod
    def name():
        return "Google TTS Module"

    @staticmethod
    def description():
        return "A module that uses Google TTS to synthesize audio."

    @staticmethod
    def input_ius():
        return [text.common.GeneratedTextIU]

    @staticmethod
    def output_iu():
        return audio.common.SpeechIU

    def __init__(self, language_code, voice_name, speaking_rate=1.4, caching=True, **kwargs):
        super().__init__(**kwargs)
        self.language_code = language_code
        self.voice_name = voice_name
        self.speaking_rate = speaking_rate
        self.caching = caching
        self.gtts = GoogleTTS(language_code, speaking_rate, caching)
        self.sample_width = 2
        self.rate = 44100


    def process_iu(self, input_iu):
        output_iu = self.create_iu(input_iu)
        raw_audio = self.gtts.tts(input_iu.get_text())
        nframes = len(raw_audio) / self.sample_width
        output_iu.set_audio(raw_audio, nframes, self.rate, self.sample_width)
        output_iu.dispatch = input_iu.dispatch
        return output_iu


