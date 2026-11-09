SELECT u.name FROM friends f JOIN users u ON (u.id = f.user2 AND f.user1 = 2) OR (u.id = f.user1 AND f.user2 = 2) ORDER BY u.name;
