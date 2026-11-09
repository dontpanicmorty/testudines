from solution import describe_params


def test_flat_redaction_and_order():
    assert describe_params({"user": "SVC", "password": "hunter2", "role": "LOADER"}) == \
        "password=***, role=LOADER, user=SVC"


def test_case_insensitive_names():
    out = describe_params({"Password": "p", "TOKEN": "t"})
    assert "p" not in out.replace("Password", "") and out == "Password=***, TOKEN=***"


def test_key_file_path_visible_key_material_hidden():
    out = describe_params({"private_key_file": "/k.p8", "private_key": "-----BEGIN"})
    assert "private_key_file=/k.p8" in out and "BEGIN" not in out


def test_nested_dict():
    out = describe_params({"session_parameters": {"QUERY_TAG": "x", "token": "secret"}, "user": "u"})
    assert out == "session_parameters={QUERY_TAG=x, token=***}, user=u"
    assert "secret" not in out


def test_input_unchanged():
    p = {"password": "p", "n": {"token": "t"}}
    describe_params(p)
    assert p == {"password": "p", "n": {"token": "t"}}
