import json

import pytest

from solution import build_params

BASE = {"SF_ACCOUNT": "org-acct", "SF_USER": "SVC"}


def test_password_auth():
    p = build_params("dev", {**BASE, "SF_PASSWORD": "x"}, "load_orders", "r1")
    assert p["account"] == "org-acct" and p["user"] == "SVC"
    assert (p["database"], p["warehouse"], p["role"]) == ("ANALYTICS_DEV", "DEV_WH", "LOADER_DEV")
    assert p["password"] == "x" and "authenticator" not in p


def test_key_pair_wins():
    p = build_params("dev", {**BASE, "SF_PASSWORD": "x", "SF_PRIVATE_KEY_PATH": "/k.p8"}, "j", "r")
    assert p["authenticator"] == "snowflake_jwt" and p["private_key_file"] == "/k.p8"
    assert "password" not in p


def test_no_credentials():
    with pytest.raises(ValueError) as info:
        build_params("dev", BASE, "j", "r")
    assert "SF_PRIVATE_KEY_PATH" in str(info.value) and "SF_PASSWORD" in str(info.value)


def test_missing_account_is_keyerror():
    with pytest.raises(KeyError):
        build_params("dev", {"SF_USER": "u", "SF_PASSWORD": "x"}, "j", "r")


def test_query_tag_is_compact_sorted_json():
    p = build_params("dev", {**BASE, "SF_PASSWORD": "x"}, "load_orders", "2026-11-02")
    tag = p["session_parameters"]["QUERY_TAG"]
    assert tag == '{"env":"dev","job":"load_orders","run":"2026-11-02"}'
    assert json.loads(tag)["job"] == "load_orders"


def test_prod_needs_opt_in():
    with pytest.raises(PermissionError):
        build_params("prod", {**BASE, "SF_PASSWORD": "x"}, "j", "r")
    assert build_params("prod", {**BASE, "SF_PASSWORD": "x"}, "j", "r", allow_prod=True)["role"] == "LOADER"


def test_admin_role_refused():
    with pytest.raises(ValueError):
        build_params("oops", {**BASE, "SF_PASSWORD": "x"}, "j", "r")
