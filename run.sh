#!/usr/bin/bash

handle_sigint() {
    echo "Received SIGINT, sending SIGINT to the background process..."
    kill "$server_pid"
    wait "$server_pid"
    exit
}

trap 'handle_sigint' SIGINT

# Run server and the bot
python3 manage.py runserver --noreload &
server_pid=$!

sleep 1

# 8000 is default django port
curl http://127.0.0.1:8000/bot/run/

wait "$server_pid"