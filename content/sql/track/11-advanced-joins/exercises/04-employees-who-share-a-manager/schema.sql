CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, department VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', 'eng', NULL),
  (2, 'Sam', 'eng', 1),
  (3, 'Lee', 'eng', 1),
  (4, 'Noor', 'eng', 1),
  (5, 'Kai', 'sales', 1);
