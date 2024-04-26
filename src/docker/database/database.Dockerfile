FROM mariadb:10.8.2

COPY database_init.sql \
    /docker-entrypoint-initdb.d/database_init.sql