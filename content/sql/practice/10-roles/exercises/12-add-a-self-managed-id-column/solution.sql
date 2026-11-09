CREATE TABLE users_roles (id INTEGER PRIMARY KEY, userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id), UNIQUE (userId, roleId));
