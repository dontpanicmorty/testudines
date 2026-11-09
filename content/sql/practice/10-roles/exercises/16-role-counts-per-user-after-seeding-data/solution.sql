CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id));
INSERT INTO users_roles VALUES (1,1),(1,2),(2,3);
SELECT u.userName, COUNT(*) AS role_count FROM users u JOIN users_roles ur ON u.id = ur.userId GROUP BY u.userName ORDER BY role_count DESC;
