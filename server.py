from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return app.send_static_file('index.html')

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/story', methods=['POST'])
def get_story():
    data = request.json
    name = data['name']
    origin = data['origin']
    strength = data['strength']
    year = data['year']

    prompt = f"Tell me a complete story about the {name} cigar from {origin}, a {strength} bodied cigar founded in {year}. Write it in the style of two friends having a real conversation over a cigar. Keep it under 400 words and make sure the story has a proper ending."

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
    return jsonify({"story": story})

    
    

if __name__ == '__main__':
    app.run(port=8080)
