SELECT managerId, SUM(salary) AS direct_report_salary_total FROM employees WHERE managerId IS NOT NULL GROUP BY managerId ORDER BY managerId;
