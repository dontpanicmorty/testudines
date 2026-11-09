CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id));
INSERT INTO users_roles VALUES (1,1),(1,2),(1,3),(2,1);
SELECT u.userName FROM users u JOIN users_roles ur ON u.id = ur.userId GROUP BY u.userName HAVING COUNT(DISTINCT ur.roleId) = (SELECT COUNT(*) FROM roles);
