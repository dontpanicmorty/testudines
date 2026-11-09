SELECT managerId, COUNT(*) AS report_count FROM employees WHERE managerId IS NOT NULL GROUP BY managerId ORDER BY managerId;
