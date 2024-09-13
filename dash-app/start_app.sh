#!/bin/bash
pkill -f 'app:server'
gunicorn app:server --bind 0.0.0.0:8050 --workers 4 --threads 2 --daemon
echo "Done!"