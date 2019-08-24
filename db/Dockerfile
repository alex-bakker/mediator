FROM postgres:10.5
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres

RUN mkdir -p /docker-entrypoint-initdb.d
RUN mkdir -p /mediator/

COPY *.sql /mediator/

COPY setup_database.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/setup_database.sh
