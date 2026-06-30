#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${APP_DB_USER} WITH PASSWORD '${APP_DB_PASSWORD}';
    GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${APP_DB_USER};
    GRANT USAGE, CREATE ON SCHEMA public TO ${APP_DB_USER};
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${APP_DB_USER};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${APP_DB_USER};

    CREATE TABLE IF NOT EXISTS documents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        text TEXT NOT NULL,
        rubrics JSONB NOT NULL,
        created_date TIMESTAMPTZ NOT NULL
    );

    CREATE TEMP TABLE tmp_docs (
        text TEXT,
        created_date TEXT,
        rubrics TEXT
    );

    COPY tmp_docs FROM '/data/posts.csv' WITH CSV HEADER;

    INSERT INTO documents (text, rubrics, created_date)
    SELECT text, replace(rubrics, '''', '"')::JSONB, created_date::TIMESTAMPTZ
    FROM tmp_docs;

    DROP TABLE tmp_docs;
EOSQL
