SELECT breed, COUNT(*) AS animal_count FROM (SELECT breed FROM dogs UNION ALL SELECT breed FROM cats) t GROUP BY breed ORDER BY animal_count DESC, breed;
