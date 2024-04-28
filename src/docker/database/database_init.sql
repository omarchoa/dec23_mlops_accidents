CREATE DATABASE IF NOT EXISTS shield_project_db;
USE shield_project_db;

CREATE TABLE IF NOT EXISTS users_table (
   login VARCHAR(25) NOT NULL,
   password VARCHAR(25),
   admin INT
);

CREATE TABLE IF NOT EXISTS f1_score_table (
   time_stamp TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
   f1_score FLOAT(17,16)
);

INSERT INTO users_table (login, password, admin)
VALUES
('admin', '4dmin', '2'),
('robot', 'Autom@t', '1'),
('fdo', 'c0ps', '0'),
('policierA', 'sherif', '0'),
('policierB', 'colombo', '0');

INSERT INTO f1_score_table (time_stamp, f1_score)
VALUES
("2024-04-24 13:14:08.123456", 0.87654321),
("2024-04-25 03:24:16.987654", 0.67654321),
("2024-04-25 18:34:32.050505", 0.7654321);
