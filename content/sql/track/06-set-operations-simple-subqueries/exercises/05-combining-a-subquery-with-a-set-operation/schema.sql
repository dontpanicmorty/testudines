CREATE OR REPLACE TABLE customers (customer_id INTEGER, region VARCHAR);
INSERT INTO customers VALUES
  (1, 'west'),
  (2, 'east'),
  (3, 'west'),
  (4, 'west');
CREATE OR REPLACE TABLE orders (order_id INTEGER, customer_id INTEGER, amount DECIMAL(10,2));
INSERT INTO orders VALUES
  (1, 1, 10.00),
  (2, 2, 50.00);
