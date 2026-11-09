def between(text, opener, closer):
    start = text.find(opener)
    if start == -1:
        return ""
    start += len(opener)
    end = text.find(closer, start)
    if end == -1:
        return ""
    return text[start:end]
