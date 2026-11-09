def clean_sender(text):
    text = text.strip()
    if "<" in text and ">" in text:
        text = text[text.index("<") + 1 : text.index(">")]
    return text.strip().lower()
