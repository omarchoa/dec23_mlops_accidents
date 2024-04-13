CREATE DATABASE IF NOT EXISTS shield_project_db;
USE shield_project_db;

CREATE TABLE IF NOT EXISTS users_table (
   login VARCHAR(25) NOT NULL,
   password VARCHAR(25),
   admin INT
);

INSERT INTO users_table (login, password, admin)
VALUES
('admin', '4dmin', '1'),
('fdo', 'c0ps', '0'),
('policierA', 'sherif', '0'),
('policierB', 'colombo', '0');