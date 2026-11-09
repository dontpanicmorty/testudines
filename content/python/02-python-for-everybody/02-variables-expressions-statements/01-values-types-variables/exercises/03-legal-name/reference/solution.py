import keyword


def can_be_variable_name(text):
    return text.isidentifier() and not keyword.iskeyword(text)
