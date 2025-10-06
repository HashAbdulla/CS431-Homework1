# RM.py
# Rate Monotonic Scheduling (fixed-priority, preemptive)
# ChatGPT-generated base, adjusted for correctness and print formatting

def rate_monotonic(tasks, sim_time=100):
    # tasks = list of dicts with {id, execution, period}
    schedule = []
    remaining = {t['id']: 0 for t in tasks}
    deadlines = {t['id']: t['period'] for t in tasks}
    arrivals = {t['id']: 0 for t in tasks}
    current = None

    for t in range(sim_time):
        # Release new tasks
        for task in tasks:
            if t == arrivals[task['id']]:
                remaining[task['id']] = task['execution']
                deadlines[task['id']] = t + task['period']
                arrivals[task['id']] += task['period']

        # Select ready tasks (remaining > 0)
        ready = [task for task in tasks if remaining[task['id']] > 0 and t < deadlines[task['id']]]
        if ready:
            # Sort by shortest period (highest RM priority)
            ready.sort(key=lambda x: x['period'])
            chosen = ready[0]
            if current != chosen['id']:
                schedule.append((chosen['id'], t))
                current = chosen['id']
            remaining[chosen['id']] -= 1
        else:
            current = None

    # Build human-readable timeline
    output = []
    for i in range(len(schedule) - 1):
        pid, start = schedule[i]
        end = schedule[i + 1][1]
        output.append((pid, start, end))
    if schedule:
        output.append((schedule[-1][0], schedule[-1][1], sim_time))

    return output


if __name__ == "__main__":
    tasks = [
        {"id": "τ1", "execution": 5, "period": 20},
        {"id": "τ2", "execution": 7, "period": 10},
        {"id": "τ3", "execution": 4, "period": 100},
    ]

    result = rate_monotonic(tasks, sim_time=20)
    print("Rate Monotonic Schedule (0–20):")
    for pid, start, end in result:
        print(f"  {pid}: [{start}–{end}]")
