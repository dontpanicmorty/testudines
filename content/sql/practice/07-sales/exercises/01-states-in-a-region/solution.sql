SELECT s.name FROM states s JOIN regions r ON s.regionId = r.id WHERE r.name = 'North' ORDER BY s.name;
