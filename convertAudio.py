import ffmpeg

def run():
    print("Converting audio...")
    ffmpeg.run(
        ffmpeg.output(
            ffmpeg.input("tests/genAudio.wav"),
            "audio-test.wav",
            ar=16000,  # Set audio sample rate
            ac=1       # Set number of audio channels
        )
    )