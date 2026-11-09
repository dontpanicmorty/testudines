WITH RECURSIVE org AS (
  SELECT id, name FROM employees WHERE managerId = 1
  UNION ALL
  SELECT e.id, e.name FROM employees e JOIN org o ON e.managerId = o.id
)
SELECT id, name FROM org ORDER BY id;
