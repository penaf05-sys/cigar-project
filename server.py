from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os
import re
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/')
def index():
    return app.send_static_file('index.html')

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/story', methods=['POST'])
@limiter.limit("10 per minute")
def get_story():
    data = request.json
    name = data['name']
    origin = data['origin']
    strength = data['strength']
    year = data['year']

    prompt = f"Write an immersive first-person story about smoking the {name} cigar from {origin}, a {strength} bodied cigar founded in {year}. You are speaking directly to the reader — they are the one holding it, cutting it, lighting it. Use 'you' throughout. Make them feel the setting, the ritual, the taste, the moment. Write it like they are living it right now. Make it emotional, sensory, and cinematic. Keep it under 400 words with a proper ending that leaves them wanting to light one up."

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    story = message.content[0].text
    story = story.replace('**', '')
    story = story.replace('# ', '')
    story = story.replace('---', '')
    story = story.replace('*', '')
    story = re.sub(r'^[A-Z][^\n]*\n', '', story).strip()
    paragraphs = [p.strip() for p in story.split('\n') if p.strip()]
    formatted = ''.join(f'<p>{p}</p>' for p in paragraphs)
    return jsonify({"story": formatted, "plain_text": story})

@app.route('/voiceover', methods=['POST'])
@limiter.limit("5 per minute")
def get_voiceover():
    data = request.json
    text = data['text']

    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "pNInz6obpgDQGcFmaJgB"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        import base64
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        return jsonify({"audio": audio_base64})
    else:
        print("ElevenLabs error:", response.status_code, response.text)
        return jsonify({"error": response.text}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)