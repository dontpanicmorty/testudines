SELECT d.name, d.breed AS dog_breed, c.breed AS cat_breed FROM dogs d JOIN cats c ON d.name = c.name ORDER BY d.name;
