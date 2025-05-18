#!/bin/sh

mkdir -p /app/tcpdump/data
mkdir -p /app/logs

tcpdump -i any port 12345 -U -w /app/tcpdump/data/dump.pcap &
TCPDUMP_PID=$!

python3 -u server.py --ip=0.0.0.0 --port=12345 2>&1 | tee /app/logs/log
PYTHON_PID=$!

# Wacht tot python stopt
wait $PYTHON_PID

# Optioneel: kill tcpdump als python stopt
kill $TCPDUMP_PID
