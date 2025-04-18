import subprocess

def run():
    print("Converting audio...")
    cmd_audio = f'ffmpeg -i "tests/genAudio.wav" -ar 16000 -ac 1 audio-test.wav'
    subprocess.run(cmd_audio, shell=True, check=True)