CREATE OR REPLACE TABLE product_catalog (product_id INTEGER, product_name VARCHAR);
INSERT INTO product_catalog VALUES
  (1, 'Widget'),
  (2, 'Gadget'),
  (3, 'Gizmo');
CREATE OR REPLACE TABLE inventory (product_id INTEGER, quantity_on_hand INTEGER);
INSERT INTO inventory VALUES
  (2, 40),
  (3, 10),
  (4, 5);
