from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os
import re
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

    # Original two-friends conversation style prompt (saved for animation script)
# prompt = f"Tell me a complete story about the {name} cigar from {origin}, a {strength} bodied cigar founded in {year}. Write it in the style of two friends having a real conversation over a cigar. Keep it under 400 words and make sure the story has a proper ending."

# First-person immersive prompt (live on site)
prompt = f"Write an immersive first-person story about smoking the {name} cigar from {origin}, a {strength} bodied cigar founded in {year}. Put the reader directly in the experience — they are the one holding it, cutting it, lighting it. Make them feel the setting, the ritual, the taste, the moment. Write it like they are living it right now. Make it emotional, sensory, and cinematic. Keep it under 400 words with a proper ending that leaves them wanting to light one up."

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
    return jsonify({"story": formatted})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)