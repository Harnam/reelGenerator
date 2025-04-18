import subprocess

def run(audio_name, ref_text_content, script_content):
    print("Generating audio...")
    cmd_tts = f'f5-tts_infer-cli --model F5TTS_v1_Base --ref_audio "{audio_name}" --ref_text "{ref_text_content}" --gen_text "{script_content}" --output_file "genAudio.wav"'
    subprocess.run(cmd_tts, shell=True, check=True)