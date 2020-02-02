#!/bin/sh
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
python create_first_data.py
exec gunicorn -b :8000 --access-logfile - --error-logfile - 'webapp:create_app()'