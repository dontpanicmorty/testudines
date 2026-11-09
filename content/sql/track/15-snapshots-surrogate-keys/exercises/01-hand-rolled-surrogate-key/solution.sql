SELECT employee_id, department, md5(COALESCE(employee_id::VARCHAR,'') || '-' || COALESCE(department,'')) AS surrogate_key FROM daily_feed_day1 ORDER BY employee_id;
