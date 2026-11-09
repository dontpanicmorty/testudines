SELECT r.name FROM regions r LEFT JOIN states st ON st.regionId = r.id LEFT JOIN employees e ON e.stateId = st.id WHERE e.id IS NULL ORDER BY r.name;
