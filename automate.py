import json
import os

import deleteFiles
import generateAudio
import convertAudio
import generateVideo
import generateSubs
import upload

# Prompt the user for a JSON file name with a default value
file_name = input("Enter the JSON file name (default: shorts.json): ") or "shorts.json"

print(f"Using file: {file_name}")

# Load the contents of the JSON file
try:
    with open(file_name, 'r') as file:
        data = json.load(file)
        print("JSON file loaded successfully.")
        # print(data)  # Print the loaded JSON data (optional)
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except json.JSONDecodeError:
    print(f"Error: The file '{file_name}' is not a valid JSON file.")

video_name = input("Enter video filename (default: video.mp4): ") or "video.mp4"
audio_name = input("Enter reference audio filename (default: audio.wav): ") or "audio.wav"
ref_text = input("Enter reference audio text (default: audio_ref.txt): ") or "audio_ref.txt"
output_name = input("Enter output filename (default: output.mp4): ") or "output.mp4"

if os.path.exists(ref_text):
    with open(ref_text, 'r') as file:
        ref_text_content = file.read()
else:
    ref_text_content = ""
    print(f"Reference text file '{ref_text}' does not exist. Proceeding with blank reference text.")

generateAudio.run(audio_name, ref_text_content, data["script"])
convertAudio.run()
generateSubs.run("audio-test.wav", "final_clean.srt")
generateVideo.run(video_name, output_name)

deleteFiles.run()

upload.upload_video(output_name, data["title"], data["description"], data["category"], data["keywords"])
