CREATE USER 'username'@'%' IDENTIFIED BY 'password'; # requires mysql admin permissions

GRANT SELECT, INSERT, UPDATE, DELETE ON `users_db`.* TO 'username'@'%';