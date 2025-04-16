import re
from faster_whisper import WhisperModel

def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def split_sentences(text):
    # Break text into sentences using punctuation
    return re.findall(r'[^.!?]+[.!?]?', text.strip())

def generate_clean_sentence_srt(audio_path, output_path="final_clean.srt", pause_buffer=0.3):
    model = WhisperModel("base.en", compute_type="auto")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)

    all_words = []
    for segment in segments:
        all_words.extend([w for w in segment.words if w.word.strip()])

    # Get the full transcript to split into sentences
    full_text = " ".join(w.word.strip() for w in all_words)
    sentences = split_sentences(full_text)

    # Assign words to sentences
    sentence_word_blocks = []
    current_idx = 0
    for sentence in sentences:
        word_list = []
        sentence_clean = sentence.strip().lower().replace("’", "'")
        while current_idx < len(all_words):
            w = all_words[current_idx]
            word_list.append(w)
            current_idx += 1
            combined = " ".join(word.word.strip().lower().replace("’", "'") for word in word_list)
            if sentence_clean.startswith(combined) and len(combined) >= len(sentence_clean.strip()) - 2:
                break
        sentence_word_blocks.append((sentence.strip(), word_list))

    # Generate SRT
    srt_lines = []
    index = 1
    for sentence_text, words in sentence_word_blocks:
        for i, word in enumerate(words):
            styled_line = []
            for j, w in enumerate(words):
                txt = w.word.strip()
                if j == i:
                    styled_line.append(f'<font color="yellow">{txt}</font>')
                else:
                    styled_line.append(txt)
            line = " ".join(styled_line)
            srt_text = f"{{\\an5}}<font size='120px'>{line}</font>"

            start = format_timestamp(word.start)
            end_time = word.end

            # Extend end time to pause or next word
            if i < len(words) - 1:
                next_start = words[i + 1].start
                if next_start - end_time < pause_buffer:
                    end_time = next_start
                else:
                    end_time += pause_buffer
            else:
                end_time += pause_buffer
            end = format_timestamp(end_time)

            srt_lines.append(f"{index}")
            srt_lines.append(f"{start} --> {end}")
            srt_lines.append(srt_text)
            srt_lines.append("")
            index += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))

    print(f"✅ Clean sentence-based, word-highlighted SRT saved to: {output_path}")

# Example usage
generate_clean_sentence_srt("audio-test.wav")
