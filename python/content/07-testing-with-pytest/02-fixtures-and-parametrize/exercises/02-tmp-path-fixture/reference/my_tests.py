import pytest

from customers import active_customers


@pytest.fixture
def csv_path(tmp_path):
    path = tmp_path / "customers.csv"
    path.write_text(
        "customer_id,name,plan\n"
        "1, Ada ,pro\n"
        "2,Grace,free\n"
        "3,Linus, FREE \n"
        "4,Barbara,Free\n"
        "5,Ken,team\n"
    )
    return path


def test_excludes_free_in_any_case(csv_path):
    names = [r["name"] for r in active_customers(csv_path)]
    assert "Grace" not in names and "Linus" not in names and "Barbara" not in names


def test_returns_full_rows_stripped_in_file_order(csv_path):
    assert active_customers(csv_path) == [
        {"customer_id": "1", "name": "Ada", "plan": "pro"},
        {"customer_id": "5", "name": "Ken", "plan": "team"},
    ]


def test_first_row_is_kept(csv_path):
    assert active_customers(csv_path)[0]["customer_id"] == "1"
