CREATE OR REPLACE TABLE employees (employee_id INTEGER, employee_name VARCHAR, manager_id INTEGER);
INSERT INTO employees VALUES
  (1, 'Priya', NULL),
  (2, 'Sam', 1),
  (3, 'Lee', 1);
CREATE OR REPLACE TABLE payroll_records (employee_id INTEGER, salary DECIMAL(10,2));
INSERT INTO payroll_records VALUES
  (1, 150000.00),
  (2, 110000.00),
  (9, 95000.00);
