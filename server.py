from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
import os

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

    prompt = f"Tell me a story about the {name} cigar from {origin}, a {strength} bodied cigar founded in {year}. Write it in the style of two friends having a real conversation over a cigar."

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return jsonify({"story": message.content[0].text})

if __name__ == '__main__':
    app.run(port=8080)