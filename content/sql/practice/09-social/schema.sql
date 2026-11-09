CREATE OR REPLACE TABLE users (id INTEGER, name VARCHAR, sex VARCHAR, joinYear INTEGER);
INSERT INTO users VALUES (1,'Ann',NULL,2020),(2,'Steve','m',2019),(3,'Mary','f',2021),(4,'Brenda','f',2018),(5,'Carlos','m',2022);

CREATE OR REPLACE TABLE friends (user1 INTEGER, user2 INTEGER);
INSERT INTO friends VALUES (1,2),(1,3),(2,3),(2,5),(4,5);
