CREATE DATABASE users_db;

USE users_db;

CREATE TABLE main_table (
	id VARCHAR(16) NOT NULL,
	username VARCHAR(16) NOT NULL,
	password VARCHAR(16) NOT NULL,
	rights BOOL NOT NULL,
	PRIMARY KEY (id)
	);

INSERT INTO main_table (id, username, password, rights)
VALUES
	("fdo", "fdo", "c0ps", 0),
	("admin", "admin", "4dmin", 1),
	("policierA", "policierA", "sherif", 0),
	("policierB", "policierB", "colombo", 0);