FROM postgres:10.5
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_USER=phoenix
ENV POSTGRES_DB=inventory
COPY sql/create_tables.sql /docker-entrypoint-initdb.d/create_tables.sql.sql