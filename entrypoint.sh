#!/bin/sh

alembic upgrade head

if [ "$APP_TYPE" = "bot" ]; then
    echo "Starting bot"
    python main.py
elif [ "$APP_TYPE" = "scheduler" ]; then
    echo "Starting scheduler"
    python schedulers.py
else
    echo "APP_TYPE not set"
fi
