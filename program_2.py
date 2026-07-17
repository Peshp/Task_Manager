import subprocess

result = subprocess.run(
    ['sudo', 'dmidecode', '--type', 'memory'],
    capture_output=True, text=True
)

stats = {}

for i in result.stdout.splitlines():
    splitted = i.strip()
    if ':' in splitted:
        key, _, value = splitted.partition(':')
        key = key.strip()
        value = value.strip()
        stats[key] = value

for key, value in stats.items():
    print(key, value)