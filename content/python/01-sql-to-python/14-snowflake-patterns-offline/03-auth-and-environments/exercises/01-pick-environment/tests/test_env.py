import pytest

import solution
from solution import environment_params


def test_dev_values():
    assert environment_params("dev") == {"database": "ANALYTICS_DEV", "warehouse": "DEV_WH", "role": "LOADER_DEV"}


def test_returns_copy():
    p = environment_params("dev")
    p["schema"] = "SCRATCH"
    assert "schema" not in environment_params("dev")
    assert "schema" not in solution.ENVIRONMENTS["dev"], "the shared table was mutated"


def test_unknown_lists_valid_names():
    with pytest.raises(ValueError) as info:
        environment_params("stagng")
    assert "dev" in str(info.value) and "prod" in str(info.value)


def test_prod_needs_opt_in():
    with pytest.raises(PermissionError):
        environment_params("prod")
    assert environment_params("prod", allow_prod=True)["warehouse"] == "PROD_WH"
