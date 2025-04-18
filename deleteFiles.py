import os

def run():
    try:
        files_to_delete = ["audio-test.wav", "final_clean.srt", "tests/genAudio.wav"]
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)
                print(f"Deleted {file}")
            else:
                print(f"{file} does not exist.")
    except Exception as e:
        print(f"Error deleting files: {e}")