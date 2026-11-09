SELECT employee_id, department, salary, valid_from, LEAD(valid_from) OVER (PARTITION BY employee_id ORDER BY valid_from) AS valid_to FROM employee_history ORDER BY employee_id, valid_from;
