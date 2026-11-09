CREATE OR REPLACE TABLE raw_payloads (id INTEGER, account_id INTEGER, payload VARCHAR);
INSERT INTO raw_payloads VALUES
 (1,1,'{"plan":"enterprise","teams":[{"team_id":10,"seats":5},{"team_id":11,"seats":3}],"features":["sso","reporting"]}'),
 (2,2,'{"plan":"growth","teams":[{"team_id":20,"seats":2}],"features":["reporting"]}'),
 (3,3,'{"plan":"starter","teams":[],"features":[]}');
