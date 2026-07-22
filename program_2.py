import subprocess

line_as_bytes = subprocess.check_output("nvidia-smi -L", shell=True)

print(line_as_bytes)