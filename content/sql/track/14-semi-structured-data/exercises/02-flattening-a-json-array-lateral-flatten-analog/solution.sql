WITH exploded AS (
  SELECT id, account_id, payload,
         unnest(CAST(payload::JSON->'teams' AS STRUCT(team_id INTEGER, seats INTEGER)[])) AS team
  FROM raw_payloads
)
SELECT id, account_id, team.team_id, team.seats
FROM exploded
ORDER BY id, team.team_id;
