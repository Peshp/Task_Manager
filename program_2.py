import psutil

mem = psutil.virtual_memory().active
total = psutil.virtual_memory().total

print(mem / 1000000000)
print(total / 1000000000)