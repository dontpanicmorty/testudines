CREATE OR REPLACE TABLE daily_feed_day1 (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2));
INSERT INTO daily_feed_day1 VALUES (1,'engineering',90000),(2,'sales',70000),(3,'marketing',65000);

CREATE OR REPLACE TABLE daily_feed_day2 (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2));
INSERT INTO daily_feed_day2 VALUES (1,'engineering',95000),(2,'sales',70000),(4,'engineering',80000);

CREATE OR REPLACE TABLE employee_history (employee_id INTEGER, department VARCHAR, salary DECIMAL(10,2), valid_from DATE);
INSERT INTO employee_history VALUES
 (1,'engineering',90000,'2023-01-01'),
 (1,'engineering',95000,'2023-06-01'),
 (2,'sales',70000,'2023-01-01');
