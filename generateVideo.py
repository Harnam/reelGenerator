import subprocess
import random
import ffmpeg

def run(video_name, output_name):

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