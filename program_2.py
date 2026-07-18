import subprocess

result = subprocess.run(
    ['lscpu'],
    capture_output=True, text=True
)

data1 = dict()
for i in result.stdout.splitlines():
    if ":" in i:
        label, value = i.split(':', 1)
        data1[label.strip()] = value.strip()

for i, v in data1.items():
    if i == 'Socket(s)':
        print(v)