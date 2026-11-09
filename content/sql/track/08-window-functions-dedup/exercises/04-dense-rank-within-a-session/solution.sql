SELECT session_id, event_id, event_ts, DENSE_RANK() OVER (PARTITION BY session_id ORDER BY event_ts) AS session_rank FROM events ORDER BY session_id, session_rank;
