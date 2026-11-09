import re


def hashtags(text):
    return re.findall(r"#[A-Za-z0-9_]+", text)
