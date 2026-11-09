CREATE OR REPLACE TABLE customers (customer_id INTEGER, customer_name VARCHAR);
INSERT INTO customers VALUES
  (1, 'Ana Lopez'),
  (2, 'Ben Kim');
CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (10, 1, 25.00),
  (11, 1, 40.00),
  (12, 2, 15.00);
