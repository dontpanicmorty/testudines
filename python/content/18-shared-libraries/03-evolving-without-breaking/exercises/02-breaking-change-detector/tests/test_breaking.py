from solution import is_breaking


def base(path, delimiter=","): ...


def test_identical():
    def same(path, delimiter=","): ...
    assert is_breaking(base, same) is False


def test_add_optional_keyword_only():
    def new(path, delimiter=",", *, encoding="utf-8"): ...
    assert is_breaking(base, new) is False


def test_add_optional_at_end():
    def new(path, delimiter=",", quote='"'): ...
    assert is_breaking(base, new) is False


def test_add_required():
    def new(path, delimiter=",", *, encoding): ...
    assert is_breaking(base, new) is True


def test_remove_parameter():
    def new(path): ...
    assert is_breaking(base, new) is True


def test_rename_parameter():
    def new(file, delimiter=","): ...
    assert is_breaking(base, new) is True


def test_reorder():
    def new(delimiter, path): ...
    assert is_breaking(base, new) is True


def test_insert_optional_in_middle():
    def new(path, encoding="utf-8", delimiter=","): ...
    assert is_breaking(base, new) is True


def test_became_keyword_only():
    def new(path, *, delimiter=","): ...
    assert is_breaking(base, new) is True


def test_default_removed():
    def new(path, delimiter): ...
    assert is_breaking(base, new) is True


def test_default_added_is_fine():
    def old(a, b): ...
    def new(a, b=1): ...
    assert is_breaking(old, new) is False
