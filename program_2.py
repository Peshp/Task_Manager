import psutil

disk = psutil.disk_usage('/')

print(disk)