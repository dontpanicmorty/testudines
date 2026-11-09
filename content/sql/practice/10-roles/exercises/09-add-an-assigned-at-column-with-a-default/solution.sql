CREATE TABLE users_roles (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id), assigned_at DATE DEFAULT CURRENT_DATE, PRIMARY KEY (userId, roleId));
