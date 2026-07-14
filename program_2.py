import psutil, time

net = psutil.net_io_counters()
print(f"Bytes sent: {net.bytes_sent}")
print(f"Bytes received: {net.bytes_recv}")