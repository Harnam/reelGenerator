import subprocess
from f5_tts import api

def run(audio_name, ref_text_content, script_content):
    
    f5tts = api.F5TTS()

    wav, sr, spect = f5tts.infer(
        audio_name,
        ref_text_content,
        script_content,
        file_wave="tests/genAudio.wav",
        seed=100,  # random seed = -1
    )