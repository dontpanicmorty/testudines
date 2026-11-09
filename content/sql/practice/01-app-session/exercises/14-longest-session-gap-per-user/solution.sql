WITH gaps AS (
  SELECT userId, sessionDate,
         DATE_DIFF('day', LAG(sessionDate) OVER (PARTITION BY userId ORDER BY sessionDate), sessionDate) AS gap_days
  FROM sessions
)
SELECT userId, MAX(gap_days) AS longest_gap
FROM gaps
WHERE gap_days IS NOT NULL
GROUP BY userId
ORDER BY userId;
