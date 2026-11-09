Create a users_roles table (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id)) using a composite PRIMARY KEY on (userId, roleId) instead of a separate UNIQUE constraint.
