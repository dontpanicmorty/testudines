`revenue_by_product(path)` should return `{product_id: total}` where total is the sum of `quantity * unit_price` over all lines for that product (as floats), reading the file **in one streaming pass**. As written it crashes or returns wrong numbers: strings are being multiplied and a part of the data goes missing. Fix it without loading the whole file into a list.

```python
# lines: P1,2,5.0  P1,1,5.0  P2,3,1.5
revenue_by_product(path)   # {"P1": 15.0, "P2": 4.5}
```
