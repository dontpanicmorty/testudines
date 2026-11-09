WITH exploded AS (
  SELECT id, account_id, payload,
         unnest(CAST(payload::JSON->'teams' AS STRUCT(team_id INTEGER, seats INTEGER)[])) AS team
  FROM raw_payloads
)
SELECT account_id, payload::JSON->>'plan' AS plan, team.team_id, team.seats,
       CASE WHEN team.seats >= 5 THEN 'large' ELSE 'small' END AS team_size_tier
FROM exploded
ORDER BY account_id, team.team_id;
