# Python

# Install required libraries:
# pip install pytube openai

from pytube import YouTube
import openai
import os
import subprocess

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def download_audio(video_url, output_file="audio.mp3"):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(filename="temp_audio")

    subprocess.run(["ffmpeg", "-y", "-i", "temp_audio", output_file], capture_output=True)
    os.remove("temp_audio")
    return output_file

def transcribe_audio(audio_file):
    with open(audio_file, "rb") as f:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text

def generate_notes(text, max_length=300):
    prompt = (
        "Extract the main points from the following transcript and create concise notes:\n"
        f"{text}"
    )

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_length,
        temperature=0.5
    )

    return response.choices[0].message["content"].strip()

def main():
    video_url = input("Enter YouTube video URL: ").strip()

    print("Downloading audio...")
    audio_file = download_audio(video_url)

    print("Transcribing audio...")
    transcript = transcribe_audio(audio_file)
    print("Transcription complete!")

    print("Generating notes...")
    notes = generate_notes(transcript)

    print("--- Notes ---")
    print(notes)

if __name__ == "__main__":
    main()
