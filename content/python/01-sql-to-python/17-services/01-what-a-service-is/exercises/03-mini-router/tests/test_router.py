from solution import Router


def make():
    r = Router()
    r.add("GET", "/orders/{order_id}", lambda order_id: (200, {"id": order_id}))
    r.add("GET", "/orders/recent", lambda: (200, {"recent": True}))
    r.add("POST", "/orders", lambda: (201, {"created": True}))
    r.add("GET", "/customers/{cid}/orders/{oid}", lambda cid, oid: (200, {"c": cid, "o": oid}))
    r.add("GET", "/", lambda: (200, {"root": True}))
    return r


def test_placeholder_capture():
    assert make().dispatch("GET", "/orders/1001") == (200, {"id": "1001"})


def test_two_placeholders():
    assert make().dispatch("GET", "/customers/5/orders/9") == (200, {"c": "5", "o": "9"})


def test_unknown_path_404():
    assert make().dispatch("GET", "/nope") == (404, {"error": "not found"})


def test_wrong_length_404():
    assert make().dispatch("GET", "/orders/1/extra")[0] == 404


def test_wrong_method_405():
    assert make().dispatch("DELETE", "/orders/1001") == (405, {"error": "method not allowed"})


def test_method_case_insensitive():
    assert make().dispatch("post", "/orders") == (201, {"created": True})


def test_trailing_slash_ignored():
    assert make().dispatch("GET", "/orders/1001/") == (200, {"id": "1001"})


def test_literal_beats_placeholder_regardless_of_registration_order():
    assert make().dispatch("GET", "/orders/recent") == (200, {"recent": True})
    r = Router()
    r.add("GET", "/a/recent", lambda: (200, {"lit": 1}))
    r.add("GET", "/a/{x}", lambda x: (200, {"x": x}))
    assert r.dispatch("GET", "/a/recent") == (200, {"lit": 1})
    assert r.dispatch("GET", "/a/other") == (200, {"x": "other"})


def test_root_route():
    assert make().dispatch("GET", "/") == (200, {"root": True})


def test_routers_are_independent():
    a, b = Router(), Router()
    a.add("GET", "/x", lambda: (200, {}))
    assert b.dispatch("GET", "/x")[0] == 404
