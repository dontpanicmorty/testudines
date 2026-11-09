SELECT d2.employee_id, d2.department FROM daily_feed_day2 d2 LEFT JOIN daily_feed_day1 d1 ON d1.employee_id = d2.employee_id WHERE d1.employee_id IS NULL ORDER BY d2.employee_id;
