Create a users_roles table (userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id)) so a user can only have a specific role once, using a UNIQUE constraint on the pair.
