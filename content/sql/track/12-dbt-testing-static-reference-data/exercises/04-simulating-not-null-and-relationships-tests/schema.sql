CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER);
INSERT INTO orders VALUES
  (1, 1),
  (2, NULL),
  (3, 2),
  (4, 99);
CREATE OR REPLACE TABLE customers (customer_id INTEGER);
INSERT INTO customers VALUES (1), (2), (3);
