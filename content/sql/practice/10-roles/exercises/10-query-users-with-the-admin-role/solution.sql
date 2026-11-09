CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id));
INSERT INTO users_roles VALUES (1, 1);
SELECT u.userName FROM users u JOIN users_roles ur ON u.id = ur.userId JOIN roles r ON r.id = ur.roleId WHERE r.role = 'admin';
