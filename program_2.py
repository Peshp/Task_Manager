import psutil

io = psutil.net_io_counters(pernic=True)
stats = psutil.net_if_stats()

targets = ["Ethernet", "Wi-Fi"]  # adjust names for your OS

for name in targets:
    if name in io:
        print(f"\n=== {name} ===")
        print(f"Up: {stats[name].isup}, Speed: {stats[name].speed} Mbps")
        print(f"Sent: {io[name].bytes_sent} bytes")
        print(f"Recv: {io[name].bytes_recv} bytes")

print(io)