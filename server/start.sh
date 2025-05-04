mkdir -p /app/tcpdump/data
tcpdump -i any  -W 5 -C 10 -w /app/tcpdump/data/dump.pcap &
python3 server.py

