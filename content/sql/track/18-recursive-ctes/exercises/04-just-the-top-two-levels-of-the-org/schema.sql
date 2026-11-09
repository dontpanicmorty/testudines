CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1),
  (4, 'Noor', 2),
  (5, 'Kai', 4);
