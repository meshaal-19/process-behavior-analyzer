import psutil
import time
from datetime import datetime
import matplotlib.pyplot as plt

CPU_THRESHOLD = 60
CPU_INTERVALS = 3
MEM_INTERVALS = 4
SAMPLE_INTERVAL = 2

previous_cpu = {}
high_cpu_count = {}

previous_mem = {}
mem_growth_count = {}

flagged_data = {}

seen_pids = set()
cpu_anomaly_count = 0
mem_anomaly_count = 0
offender_count = {}

start_time = time.time()

print("Process Behavior Analyzer started")
print("Monitoring process behavior...")
print("Press Ctrl+C to stop and view graphs\n")

for p in psutil.process_iter():
    try:
        p.cpu_percent(None)
    except:
        pass

try:
    while True:
        print("PID\tCPU%\tΔCPU\tMEM%\tSTATE\tNAME")
        print("-" * 90)

        for process in psutil.process_iter(['pid', 'name']):
            try:
                pid = process.info['pid']
                name = process.info['name']

                if pid == 0 or name == "System Idle Process":
                    continue

                seen_pids.add(pid)

                cpu = process.cpu_percent(None)
                mem = process.memory_percent()
                state = process.status()

                last_cpu = previous_cpu.get(pid, 0.0)
                delta_cpu = cpu - last_cpu
                previous_cpu[pid] = cpu

                if cpu > CPU_THRESHOLD:
                    high_cpu_count[pid] = high_cpu_count.get(pid, 0) + 1
                else:
                    high_cpu_count[pid] = 0

                last_mem = previous_mem.get(pid, mem)
                if mem > last_mem:
                    mem_growth_count[pid] = mem_growth_count.get(pid, 0) + 1
                else:
                    mem_growth_count[pid] = 0
                previous_mem[pid] = mem

                status = []
                now = time.time() - start_time

                if high_cpu_count[pid] >= CPU_INTERVALS:
                    status.append("⚠ HIGH CPU")
                    cpu_anomaly_count += 1
                    offender_count[name] = offender_count.get(name, 0) + 1
                    with open("behavior_log.txt", "a") as log:
                        log.write(
                            f"{datetime.now()} | PID {pid} | {name} | CPU {cpu:.1f}% | Sustained High CPU\n"
                        )

                if mem_growth_count[pid] >= MEM_INTERVALS:
                    status.append("⚠ MEMORY GROWTH")
                    mem_anomaly_count += 1
                    offender_count[name] = offender_count.get(name, 0) + 1
                    with open("behavior_log.txt", "a") as log:
                        log.write(
                            f"{datetime.now()} | PID {pid} | {name} | MEM {mem:.2f}% | Sustained Memory Growth\n"
                        )

                if status:
                    if pid not in flagged_data:
                        flagged_data[pid] = {
                            "name": name,
                            "time": [],
                            "cpu": [],
                            "mem": []
                        }
                    flagged_data[pid]["time"].append(now)
                    flagged_data[pid]["cpu"].append(cpu)
                    flagged_data[pid]["mem"].append(mem)

                if cpu > 0 or mem > 0:
                    print(
                        f"{pid}\t{cpu:.1f}\t{delta_cpu:+.1f}\t{mem:.2f}\t{state}\t{name} {' '.join(status)}"
                    )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        time.sleep(SAMPLE_INTERVAL)
        print("\n")

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.\n")

print("=== Execution Summary ===")
print(f"Total processes monitored: {len(seen_pids)}")
print(f"CPU anomalies detected: {cpu_anomaly_count}")
print(f"Memory anomalies detected: {mem_anomaly_count}")

if offender_count:
    worst = max(offender_count, key=offender_count.get)
    print(f"Most frequent offender: {worst}")
else:
    print("Most frequent offender: None")

print("\nGenerating graphs for flagged processes...\n")

for pid, data in flagged_data.items():
    if not data["time"]:
        continue

    plt.figure()
    plt.plot(data["time"], data["cpu"], label="CPU %")
    plt.plot(data["time"], data["mem"], label="Memory %")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Usage (%)")
    plt.title(f"CPU & Memory Usage Over Time\n{data['name']} (PID {pid})")
    plt.legend()
    plt.tight_layout()
    plt.show()
