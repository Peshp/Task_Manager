import subprocess

def get_uevent_info(interface_name):
    result = subprocess.run(
        ["ethtool", "-i", interface_name],
        capture_output=True, text=True
    )
    info = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

info = get_uevent_info("wlo1")
slot = info.get("bus-info")   # correct key, e.g. "0000:00:14.3"

# print each key-value pair on its own line
for key, val in info.items():
    print(f"{key}: {val}")