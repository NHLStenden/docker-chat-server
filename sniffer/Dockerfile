FROM nicolaka/netshoot
WORKDIR /app
CMD mkdir -p /app/tcpdump/data && \
    tcpdump -i any port 12345  -U -w /app/tcpdump/data/dump.pcap
