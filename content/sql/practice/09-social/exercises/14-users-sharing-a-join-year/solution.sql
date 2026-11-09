SELECT u1.name AS name1, u2.name AS name2 FROM users u1 JOIN users u2 ON u1.joinYear = u2.joinYear AND u1.name < u2.name ORDER BY name1;
