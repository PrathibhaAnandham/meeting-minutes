import os
import torch
import whisper
import torchaudio
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK resources (first-time only)
nltk.download("vader_lexicon")

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set torchaudio backend explicitly
torchaudio.set_audio_backend("sox_io")  # Alternative: "soundfile" if sox_io fails

# Load Whisper Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("small", device=device)

# Allowed file type check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to summarize text using Sumy
def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary_sentences])

# Function to perform sentiment analysis using VADER
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score["compound"] >= 0.05:
        return "Positive"
    elif sentiment_score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to extract key points (using simple TextRank)
def extract_key_points(text):
    sentences = text.split(". ")
    return sentences[:3]  # Take first 3 sentences as key points (basic method)

# Function to extract action items (detect sentences with "must", "should", etc.)
def extract_action_items(text):
    sentences = text.split(". ")
    action_items = [sentence for sentence in sentences if "must" in sentence or "should" in sentence or "need to" in sentence]
    return action_items if action_items else ["No specific action items identified."]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .wav file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(filepath)
        print(f"File saved successfully at {filepath}")  # Debugging output

        # Normalize path for Windows
        filepath = os.path.abspath(filepath)

        # Check if file is empty
        if os.path.getsize(filepath) == 0:
            return jsonify({'error': 'Uploaded file is empty or corrupted. Please try again.'})

        # Verify if the audio file can be loaded
        try:
            waveform, sample_rate = torchaudio.load(filepath)
            print(f"File loaded successfully: Sample Rate={sample_rate}, Shape={waveform.shape}")
        except Exception as e:
            return jsonify({'error': f'Error loading audio file: {str(e)}'})

        # Transcribe audio
        result = model.transcribe(filepath)
        transcription = result['text']

        # Generate additional outputs
        summary = summarize_text(transcription)
        sentiment = analyze_sentiment(transcription)
        key_points = extract_key_points(transcription)
        action_items = extract_action_items(transcription)

        response = {
            'message': 'File processed successfully',
            'transcription': transcription,
            'summary': summary,
            'sentiment': sentiment,
            'key_points': key_points,
            'action_items': action_items
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
