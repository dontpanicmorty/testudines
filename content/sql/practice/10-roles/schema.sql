CREATE OR REPLACE TABLE users (id INTEGER PRIMARY KEY, userName VARCHAR NOT NULL);
INSERT INTO users VALUES (1,'alice'),(2,'bob'),(3,'carol');

CREATE OR REPLACE TABLE roles (id INTEGER PRIMARY KEY, role VARCHAR NOT NULL);
INSERT INTO roles VALUES (1,'admin'),(2,'editor'),(3,'viewer');
