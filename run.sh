#!/usr/bin/bash
# Run server and the bot
python3 manage.py runserver --noreload &
sleep 1

# 8000 is default django port
curl http://127.0.0.1:8000/bot/run/

wait