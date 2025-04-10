from transcription import transcribe_audio
from summarization import summarize_text
from key_points_extraction import extract_key_points
from action_items_extraction import extract_action_items
from sentiment_analysis import sentiment_analysis
from save_as_docx import save_as_docx

def meeting_minutes(transcription):
    summary = summarize_text(transcription)
    key_points = extract_key_points(transcription)
    action_items = extract_action_items(transcription)
    sentiment = sentiment_analysis(transcription)

    return {
        'abstract_summary': summary,
        'key_points': key_points,
        'action_items': action_items,
        'sentiment': sentiment
    }

# Run the meeting minutes generator
audio_file_path = audio_file_path = "C:/Users/prath/OneDrive/Desktop/miniproj/meeting-minutes/audio/EarningsCall.wav"

transcription = transcribe_audio(audio_file_path)
minutes = meeting_minutes(transcription)

print(minutes)
save_as_docx(minutes, 'meeting_minutes.docx')
