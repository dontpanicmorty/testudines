from solution import table_rows


def test_basic():
    html = "<table><tr><th>Item</th><th>Qty</th></tr><tr><td>tea</td><td> 3 </td></tr></table>"
    assert table_rows(html) == [["Item", "Qty"], ["tea", "3"]]


def test_no_table():
    assert table_rows("<p>hi</p>") == []


def test_only_first_table():
    html = "<table><tr><td>a</td></tr></table><table><tr><td>b</td></tr></table>"
    assert table_rows(html) == [["a"]]


def test_whitespace_and_newlines():
    html = "<table>\n<tr>\n<td>\n x \n</td>\n<td>y</td>\n</tr>\n</table>"
    assert table_rows(html) == [["x", "y"]]


def test_empty_cell_kept():
    html = "<table><tr><td></td><td>y</td></tr></table>"
    assert table_rows(html) == [["", "y"]]
