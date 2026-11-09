from solution import word_frequencies


def write(tmp_path, text):
    p = tmp_path / "t.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_case_and_punctuation(tmp_path):
    p = write(tmp_path, "Tea, tea! TEA?\n")
    assert word_frequencies(p) == {"tea": 3}


def test_apostrophe_removed(tmp_path):
    p = write(tmp_path, "Don't stop. Dont!\n")
    assert word_frequencies(p) == {"dont": 2, "stop": 1}


def test_lone_punctuation_ignored(tmp_path):
    p = write(tmp_path, "a -- b\n")
    assert word_frequencies(p) == {"a": 1, "b": 1}


def test_empty(tmp_path):
    assert word_frequencies(write(tmp_path, "")) == {}


def test_multiple_lines(tmp_path):
    p = write(tmp_path, "The cat.\nthe DOG;\n")
    assert word_frequencies(p) == {"the": 2, "cat": 1, "dog": 1}
