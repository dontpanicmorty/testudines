SELECT d2.employee_id, d2.department, d2.salary
FROM daily_feed_day2 d2
JOIN daily_feed_day1 d1 ON d1.employee_id = d2.employee_id
WHERE d1.department IS DISTINCT FROM d2.department OR d1.salary IS DISTINCT FROM d2.salary
ORDER BY d2.employee_id;
