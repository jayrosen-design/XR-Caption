import openai
import os
import requests
import uuid
from flask import Flask, request, jsonify, send_file, render_template


# Add your OpenAI API key
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

# Add your ElevenLabs API key
ELEVENLABS_API_KEY = ""

ELEVENLABS_VOICE_STABILITY = 0.30
ELEVENLABS_VOICE_SIMILARITY = 0.75

# Choose your favorite ElevenLabs voice
ELEVENLABS_VOICE_NAME = "Marie"
ELEVENLABS_ALL_VOICES = []

app = Flask(__name__)

def transcribe_audio(filename: str) -> str:
    """Transcribe audio to text.

    :param filename: The path to an audio file.
    :returns: The transcribed text of the file.
    :rtype: str

    """
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return 'No file found', 400
    file = request.files['file']
    recording_file = f"{uuid.uuid4()}.wav"
    recording_path = f"uploads/{recording_file}"
    os.makedirs(os.path.dirname(recording_path), exist_ok=True)
    file.save(recording_path)
    transcription = transcribe_audio(recording_path)
    
    return jsonify({'text': transcription})

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html', voice=ELEVENLABS_VOICE_NAME)

@app.route('/stereo')
def stereo():
    """Render the stereoscopic page."""
    return render_template('stereo.html', voice=ELEVENLABS_VOICE_NAME)


if __name__ == '__main__':
    app.run()
