def extract_action_items(text):
    action_phrases = ["we need to", "we should", "let's", "our next step is", "it is necessary to"]
    action_items = []

    for sentence in text.split("."):
        for phrase in action_phrases:
            if phrase in sentence.lower():
                action_items.append(sentence.strip())

    return action_items
