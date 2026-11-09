SELECT sub_id, effective_date, status,
   CASE WHEN LAG(status) OVER (PARTITION BY sub_id ORDER BY effective_date) IS DISTINCT FROM status THEN true ELSE false END AS status_changed
FROM subscription_history
ORDER BY sub_id, effective_date;
