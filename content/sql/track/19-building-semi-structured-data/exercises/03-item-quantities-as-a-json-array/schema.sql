CREATE OR REPLACE TABLE order_items (order_id INTEGER, product_name VARCHAR, quantity INTEGER);
INSERT INTO order_items VALUES
  (1, 'Widget', 2),
  (1, 'Gadget', 1),
  (2, 'Gizmo', 5),
  (2, 'Widget', 3),
  (2, 'Gadget', 4);
