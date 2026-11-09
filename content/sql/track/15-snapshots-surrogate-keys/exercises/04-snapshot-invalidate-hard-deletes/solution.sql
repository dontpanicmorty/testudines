SELECT d1.employee_id FROM daily_feed_day1 d1 LEFT JOIN daily_feed_day2 d2 ON d1.employee_id = d2.employee_id WHERE d2.employee_id IS NULL ORDER BY d1.employee_id;
