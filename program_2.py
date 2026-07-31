import psutil
import time


def poll():
    # ---- Network interfaces ----
    network_list = []
    for name, stats in psutil.net_if_stats().items():
        network_list.append({
            'Network': name,
            'Status': 'Up' if stats.isup else 'Down',
            'Speed': f'{stats.speed} Mbps' if stats.speed else 'N/A'
        })

    # ---- Memory ----
    vm = psutil.virtual_memory()
    memory_data = {
        'Total': vm.total / 1e9,
        'Used': vm.used / 1e9,
        'Available': vm.available / 1e9,
        'Percent': vm.percent
    }

    # ---- Processes ----
    proc = []
    for pid in psutil.pids()[-200:]:
        try:
            p = psutil.Process(pid)
            p.cpu_percent()  # first call primes the measurement
            proc.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    time.sleep(0.1)

    top = {}
    for p in proc:
        try:
            top[p] = p.cpu_percent() / psutil.cpu_count()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_list = sorted(top.items(), key=lambda x: x[1])
    top10 = top_list[-10:]
    top10.reverse()

    cpu_rows = []
    for p, cpu_percent in top10:
        try:
            with p.oneshot():
                cpu_rows.append({
                    'PID': p.pid,
                    'Name': p.name(),
                    'Status': p.status(),
                    'CPU%': f'{cpu_percent:.2f}%',
                    'Threads': p.num_threads(),
                    'Mem(MB)': f'{p.memory_info().rss / 1e6:.2f}'
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # ---- Print everything nicely ----
    _print_network(network_list)
    _print_memory(memory_data)
    _print_processes(cpu_rows)


def _print_network(network_list):
    print("\n" + "=" * 50)
    print(" NETWORK INTERFACES")
    print("=" * 50)
    print(f"{'Name':<15}{'Status':<10}{'Speed':<15}")
    print("-" * 50)
    for n in network_list:
        print(f"{n['Network']:<15}{n['Status']:<10}{n['Speed']:<15}")


def _print_memory(memory_data):
    print("\n" + "=" * 50)
    print(" MEMORY")
    print("=" * 50)
    print(f"Total:     {memory_data['Total']:.2f} GB")
    print(f"Used:      {memory_data['Used']:.2f} GB")
    print(f"Available: {memory_data['Available']:.2f} GB")
    print(f"Percent:   {memory_data['Percent']}%")


def _print_processes(cpu_rows):
    print("\n" + "=" * 70)
    print(" TOP 10 PROCESSES BY CPU")
    print("=" * 70)
    header = f"{'PID':<8}{'Name':<20}{'Status':<12}{'CPU%':<10}{'Threads':<10}{'Mem(MB)':<10}"
    print(header)
    print("-" * 70)
    for row in cpu_rows:
        print(f"{row['PID']:<8}{row['Name']:<20}{row['Status']:<12}"
              f"{row['CPU%']:<10}{row['Threads']:<10}{row['Mem(MB)']:<10}")

print(poll())