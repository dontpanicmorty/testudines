CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id));
INSERT INTO users_roles VALUES (1,1),(2,2);
SELECT u.userName FROM users u WHERE u.id NOT IN (SELECT userId FROM users_roles WHERE roleId = 3);
