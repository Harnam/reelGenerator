import os
import subprocess
import random
import shutil
import sys
import ffmpeg

import generateAudio
import convertAudio
import generateVideo

# Function to ask user if they want to delete generated files
def del_files():
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

# Check if ffmpeg is installed
if shutil.which("ffmpeg") is None:
    print("Error: ffmpeg is not installed. Please install it using Homebrew:")
    print("  brew install ffmpeg")
    sys.exit(1)

# Ask for filenames with defaults
video_name = input("Enter video filename (default: video.mp4): ") or "video.mp4"
audio_name = input("Enter reference audio filename (default: audio.wav): ") or "audio.wav"
ref_text = input("Enter reference audio text (default: audio_ref.txt): ") or "audio_ref.txt"
script_name = input("Enter script text filename (default: script.txt): ") or "script.txt"
output_name = input("Enter output filename (default: output.mp4): ") or "output.mp4"

delete_files = input("Do you want to delete the generated files? (yes/no): ").strip().lower()

# Read contents of ref_text file
if os.path.exists(ref_text):
    with open(ref_text, 'r') as file:
        ref_text_content = file.read()
else:
    ref_text_content = ""
    print(f"Reference text file '{ref_text}' does not exist. Proceeding with blank reference text.")

# Read contents of script_name file
if os.path.exists(script_name):
    with open(script_name, 'r') as file:
        script_content = file.read()
        script_content = script_content.replace("\n", ". ")
else:
    script_content = ""
    print(f"Script file '{script_name}' does not exist. Proceeding with blank script content.")

# Step 1: Generate audio
generateAudio.run(audio_name, ref_text_content, script_content)

# Step 2: Convert audio
convertAudio.run()

# Step 3: Run proper.py
print("Running proper.py...")
subprocess.run("python3 proper.py", shell=True, check=True)

# Step 4: Generate random timestamp (0 to 10 minutes)
generateVideo.run(video_name, output_name)

if delete_files in ["yes", "y"]:
    del_files()
else:
    print("Generated files were not deleted.")

print(f"✅ Done! Output saved as {output_name}")
