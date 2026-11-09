import json
import os
from pathlib import Path

from solution import downstream_models

M = {
    "nodes": {
        "model.shop.stg_orders": {"depends_on": {"nodes": ["source.shop.raw.orders"]}},
        "model.shop.int_totals": {"depends_on": {"nodes": ["model.shop.stg_orders"]}},
        "model.shop.fct_sales": {"depends_on": {"nodes": ["model.shop.int_totals", "model.shop.stg_orders"]}},
        "test.shop.not_null": {"depends_on": {"nodes": ["model.shop.fct_sales"]}},
        "model.shop.lonely": {},
        "model.shop.empty": {"depends_on": {}},
    }
}


def test_transitive():
    assert downstream_models(M, "model.shop.stg_orders") == [
        "model.shop.fct_sales",
        "model.shop.int_totals",
    ]


def test_from_source_not_in_nodes():
    assert downstream_models(M, "source.shop.raw.orders") == [
        "model.shop.fct_sales",
        "model.shop.int_totals",
        "model.shop.stg_orders",
    ]


def test_leaf_has_no_downstream_models():
    assert downstream_models(M, "model.shop.fct_sales") == []


def test_unknown_node():
    assert downstream_models(M, "model.shop.nope") == []


def test_cycle_does_not_hang():
    cyc = {"nodes": {"model.a": {"depends_on": {"nodes": ["model.b"]}}, "model.b": {"depends_on": {"nodes": ["model.a"]}}}}
    assert downstream_models(cyc, "model.a") == ["model.b"]


def test_bundled_manifest_runs():
    data = Path(os.environ["DOJO_DATA"]) / "manifest_sample.json"
    manifest = json.loads(data.read_text(encoding="utf-8"))
    for uid in manifest["nodes"]:
        res = downstream_models(manifest, uid)
        assert res == sorted(res)
        assert uid not in res
