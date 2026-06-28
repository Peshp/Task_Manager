import psutil
import numpy as np
import matplotlib.pyplot as plt

for i in range(100000000):
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    print(cpu_usage)
    print(mem_usage)

    plt.scatter(i, cpu_usage, color = "red")
    plt.scatter(i, mem_usage, color = "blue")
    plt.legend(["CPU", "Memory"], loc ="lower right")
    plt.pause(0.05)

plt.show()