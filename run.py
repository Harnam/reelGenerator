import os
import subprocess
import random
import shutil
import sys
import ffmpeg
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
print("Generating audio...")
cmd_tts = f'f5-tts_infer-cli --model F5TTS_v1_Base --ref_audio "{ audio_name }" --ref_text "{ ref_text_content }" --gen_text "{ script_content }" --output_file "genAudio.wav"'
subprocess.run(cmd_tts, shell=True, check=True)

# Step 2: Convert audio
print("Converting audio...")
cmd_audio = f'ffmpeg -i "tests/genAudio.wav" -ar 16000 -ac 1 audio-test.wav'
subprocess.run(cmd_audio, shell=True, check=True)

# Step 3: Run proper.py
print("Running proper.py...")
subprocess.run("python3 proper.py", shell=True, check=True)

# Step 4: Generate random timestamp (0 to 10 minutes)
# Get the duration of the video file
video_info = ffmpeg.probe(video_name)
video_duration = float(video_info['format']['duration'])

# Get the duration of the generated audio file
audio_info = ffmpeg.probe("tests/genAudio.wav")
audio_duration = float(audio_info['format']['duration'])

# Calculate the maximum start time
max_start_time = max(0, video_duration - audio_duration)

# Generate a random timestamp within the valid range
random_seconds = random.uniform(0, max_start_time)
hours = int(random_seconds // 3600)
minutes = int((random_seconds % 3600) // 60)
seconds = int(random_seconds % 60)
timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"
print(f"Generated random timestamp: {timestamp}")

# Step 5: Final ffmpeg command
print("Combining video and audio...")
cmd_final = (
    f'ffmpeg -ss {timestamp} -i "{video_name}" -i "tests/genAudio.wav" '
    '-vf "subtitles=final_clean.srt" -map 0:v:0 -map 1:a:0 '
    f'-c:v libx264 -c:a aac -b:a 192k -shortest {output_name}'
)
subprocess.run(cmd_final, shell=True, check=True)

if delete_files in ["yes", "y"]:
    del_files()
else:
    print("Generated files were not deleted.")

print(f"✅ Done! Output saved as {output_name}")
