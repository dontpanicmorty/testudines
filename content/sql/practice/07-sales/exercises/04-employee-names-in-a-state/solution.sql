SELECT e.name FROM employees e JOIN states s ON e.stateId = s.id WHERE s.name = 'Minnesota' ORDER BY e.name;
