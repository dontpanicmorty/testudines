CREATE SEQUENCE seq_users_roles_id START 1; CREATE TABLE users_roles (id INTEGER DEFAULT nextval('seq_users_roles_id'), userId INTEGER REFERENCES users(id), roleId INTEGER REFERENCES roles(id));
