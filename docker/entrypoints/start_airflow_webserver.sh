#!/bin/bash
# Script that allows the users and connections creations for Airflow service.

poetry run airflow db init

if [ "$AIRFLOW_CREATE_USER_CONN" = true ]; then
    # Create User
    echo "Creating airflow user..."
    poetry run airflow users create -r "$AIRFLOW_ROLE" -u "$AIRFLOW_USER" -p "$AIRFLOW_PASSWORD" -f "$AIRFLOW_FIRST" -l "$AIRFLOW_LAST" -e "$AIRFLOW_EMAIL"

    # Create PG RDS connection
    echo 'Adding PG connection into Airflow service..'
    poetry run airflow connections add "$POSTGRES_CONN_ID" \
        --conn-type 'postgres' \
        --conn-login "$POSTGRES_USER" \
        --conn-password "$POSTGRES_PASSWORD" \
        --conn-host "$POSTGRES_HOST" \
        --conn-port "$AIRFLOW_POSTGRES_PORT" \
        --conn-schema "$POSTGRES_DB"

fi
poetry run airflow webserver
