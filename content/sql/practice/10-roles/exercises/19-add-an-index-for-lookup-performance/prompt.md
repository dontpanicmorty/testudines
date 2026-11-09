Create the constrained users_roles table (userId, roleId REFERENCES, composite PRIMARY KEY), then add a separate index on roleId alone to speed up 'which users have role X' lookups.
