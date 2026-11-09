WITH RECURSIVE hierarchy AS (
  SELECT id, name, 0 AS depth FROM employees WHERE managerId IS NULL
  UNION ALL
  SELECT e.id, e.name, h.depth + 1 FROM employees e JOIN hierarchy h ON e.managerId = h.id
)
SELECT id, name, depth FROM hierarchy ORDER BY depth, id;
