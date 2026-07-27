import socket
import ipaddress

hostname = socket.gethostname()
IPAddr =ipaddress.ip_address(hostname)

print("Your Computer Name is:", hostname)
print("Your Computer IP Address is:", IPAddr)