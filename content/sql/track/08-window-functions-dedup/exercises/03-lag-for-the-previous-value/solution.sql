SELECT sub_id, effective_date, status, LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) AS previous_status FROM subscription_history ORDER BY sub_id, effective_date;
