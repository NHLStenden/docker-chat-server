FROM nicolaka/netshoot
WORKDIR /app
CMD mkdir -p /app/tcpdump/data && \
    tcpdump -i eth0 -W 5 -C 10 -w /app/tcpdump/data/dump.pcap
