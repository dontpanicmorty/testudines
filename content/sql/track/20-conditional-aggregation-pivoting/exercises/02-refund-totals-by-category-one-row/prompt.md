A returns desk logs every refunded item in `product_returns`:

CREATE TABLE product_returns (return_id INTEGER, product_category VARCHAR, refund_amount DECIMAL(10,2));
INSERT INTO product_returns VALUES
  (1, 'electronics', 120.00),
  (2, 'apparel', 40.00),
  (3, 'electronics', 80.00),
  (4, 'home_goods', 60.00),
  (5, 'apparel', 25.00),
  (6, 'electronics', 15.00),
  (7, 'home_goods', 90.00);

Management wants one summary row (not one row per category) with a separate column for each category's total refund amount: `electronics`, `apparel`, and `home_goods`.

For this sample data, the single output row should read: electronics = 215.00, apparel = 65.00, home_goods = 150.00.
