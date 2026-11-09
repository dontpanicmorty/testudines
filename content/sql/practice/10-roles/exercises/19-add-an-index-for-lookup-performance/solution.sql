CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id), PRIMARY KEY (userId, roleId)); CREATE INDEX idx_users_roles_roleid ON users_roles (roleId);
