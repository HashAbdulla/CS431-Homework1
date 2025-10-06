from dataclasses import dataclass
from typing import List, Dict
from collections import deque

@dataclass(order=True)
class Process:
    pid: str
    arrival: int
    burst: int

def round_robin(processes: List[Process], quantum: int = 2):
    processes = sorted(processes, key=lambda p: (p.arrival, p.pid))
    ready = deque()
    remaining = {p.pid: p.burst for p in processes}
    completion: Dict[str, int] = {}
    schedule = []

    t = 0
    i = 0  # next arrival index

    while i < len(processes) or ready:
        # Admit all processes that have arrived by time t
        while i < len(processes) and processes[i].arrival <= t:
            ready.append(processes[i])
            i += 1

        if not ready:
            t = processes[i].arrival
            continue

        current = ready.popleft()
        start = t
        run_time = min(quantum, remaining[current.pid])
        t += run_time
        end = t

        schedule.append((current.pid, start, end))
        remaining[current.pid] -= run_time

        # Admit newly arrived processes during execution
        while i < len(processes) and processes[i].arrival <= t:
            ready.append(processes[i])
            i += 1

        # Requeue unfinished process
        if remaining[current.pid] > 0:
            ready.append(current)
        else:
            completion[current.pid] = end

    return schedule, completion

def turnaround_times(processes: List[Process], completion: Dict[str, int]):
    return {p.pid: completion[p.pid] - p.arrival for p in processes}

def avg_tat(tats: Dict[str, int]):
    return sum(tats.values()) / len(tats)

if __name__ == "__main__":
    # === Figure 2 Dataset ===
    processes = [
        Process("P1", 0, 2),
        Process("P2", 1, 1),
        Process("P3", 2, 8),
        Process("P4", 3, 4),
        Process("P5", 4, 5)
    ]

    schedule, completion = round_robin(processes, quantum=2)
    tats = turnaround_times(processes, completion)
    att = avg_tat(tats)

    print("\nRound Robin Scheduling (Q = 2)")
    print("===================================")
    for pid, start, end in schedule:
        print(f"{pid}: [{start} – {end}]")
    print("\nCompletion Times:", completion)
    print("Turnaround Times:", tats)
    print(f"\nAverage Turnaround Time (ATT): {att:.2f}")
