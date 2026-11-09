Write `table_rows(html)` that reads the first HTML table in `html` using BeautifulSoup and returns a list of rows, where each row is a list of the cell texts (from both `<th>` and `<td>` cells) with surrounding whitespace removed. If there is no table, return `[]`.

```python
table_rows("<table><tr><th>Item</th><th>Qty</th></tr><tr><td>tea</td><td> 3 </td></tr></table>")
# [["Item", "Qty"], ["tea", "3"]]
```
