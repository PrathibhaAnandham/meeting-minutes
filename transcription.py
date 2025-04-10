import whisper

def transcribe_audio(audio_file_path):
    model = whisper.load_model("base")  # Local model
    result = model.transcribe(audio_file_path)
    return result["text"]
