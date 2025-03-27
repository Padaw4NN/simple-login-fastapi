FROM postgres:latest

ENV POSTGRES_DB credentials
ENV POSTGRES_USER admin
ENV POSTGRES_PASSWORD admin

COPY ./init.sql /docker-entrypoint-initdb.d/

RUN chown -R postgres:postgres /docker-entrypoint-initdb.d/ \
    && chmod -R 775 /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]
