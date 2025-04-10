import spacy

nlp = spacy.load("en_core_web_sm")

def extract_key_points(text, num_points=5):
    doc = nlp(text)
    key_phrases = set()

    for chunk in doc.noun_chunks:
        key_phrases.add(chunk.text.lower())

    return list(key_phrases)[:num_points]
