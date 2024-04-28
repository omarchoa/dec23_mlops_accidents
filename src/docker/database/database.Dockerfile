FROM mariadb:10.8.2

ENV MARIADB_ROOT_PASSWORD="password"
ENV MARIADB_DATABASE="shield_project_db"
ENV MARIADB_USER="user"
ENV MARIADB_PASSWORD="password"

COPY database_init.sql \
    /docker-entrypoint-initdb.d/database_init.sql