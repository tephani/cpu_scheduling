import matplotlib.pyplot as plt
import pandas as pd


def gantt_chart_with_table(schedule, title, metrics_df):
    """Visualize the Gantt Chart with a table for metrics."""
    start_times = [s[1] for s in schedule]
    process_ids = [f"P{s[0]}" for s in schedule]
    execution_times = [s[2] - s[1] for s in schedule]

    fig, ax = plt.subplots(
        1, 2, figsize=(12, 6)
    )  # Create a 1x2 subplot for Gantt chart and metrics table

    # Gantt Chart
    ax[0].barh(
        process_ids,
        execution_times,
        left=start_times,
        color="skyblue",
        edgecolor="black",
    )
    for i in range(len(schedule)):
        ax[0].text(
            start_times[i] + execution_times[i] / 2,
            i,
            f"P{schedule[i][0]}",
            ha="center",
            va="center",
        )

    ax[0].set_title(title)
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Processes")
    ax[0].grid(True)

    # Display the metrics table on the right
    ax[1].axis("off")  # Hide the axes for the table
    table = ax[1].table(
        cellText=metrics_df.values, colLabels=metrics_df.columns, loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Adjust the size of the table

    plt.tight_layout()
    plt.show()


def calculate_metrics(processes, completion_times):
    """Calculate TAT and WT for all processes and return a pandas DataFrame."""
    n = len(processes)
    turnaround_times = [completion_times[i] - processes[i][0] for i in range(n)]
    waiting_times = [turnaround_times[i] - processes[i][1] for i in range(n)]

    # Calculate the averages and round to a whole number
    avg_tat = round(sum(turnaround_times) / n)
    avg_wt = round(sum(waiting_times) / n)

    # Create a DataFrame for the metrics
    data = {
        "Process": [f"P{i+1}" for i in range(n)],
        "Arrival Time": [processes[i][0] for i in range(n)],
        "Burst Time": [processes[i][1] for i in range(n)],
        "Completion Time": completion_times,
        "Turnaround Time (TAT)": turnaround_times,
        "Waiting Time (WT)": waiting_times,
    }

    metrics_df = pd.DataFrame(data)

    # Print the metrics in a table format
    print("\nProcess\tArrival\tBurst\tCompletion\tTAT\tWT")
    for i in range(n):
        print(
            f"P{i+1}\t\t{processes[i][0]}\t\t{processes[i][1]}\t\t{completion_times[i]}\t\t{turnaround_times[i]}\t\t{waiting_times[i]}"
        )

    print(f"\nAverage Turnaround Time: {avg_tat}")
    print(f"Average Waiting Time: {avg_wt}")

    # Create a DataFrame for the averages
    avg_data = pd.DataFrame(
        [
            {
                "Process": "Average",
                "Arrival Time": "",
                "Burst Time": "",
                "Completion Time": "",
                "Turnaround Time (TAT)": avg_tat,
                "Waiting Time (WT)": avg_wt,
            }
        ]
    )

    # Concatenate the new average row to the original metrics DataFrame
    metrics_df = pd.concat([metrics_df, avg_data], ignore_index=True)

    return metrics_df


def fcfs(processes):
    """First-Come-First-Serve Scheduling (Non-Preemptive)."""
    processes.sort(key=lambda x: x[0])  # Sort by arrival time
    completion_times = []
    current_time = 0
    schedule = []

    for i, (arrival, burst) in enumerate(processes):
        if current_time < arrival:
            current_time = arrival
        start_time = current_time
        current_time += burst
        completion_times.append(current_time)
        schedule.append((i + 1, start_time, current_time))

    metrics_df = calculate_metrics(processes, completion_times)
    gantt_chart_with_table(schedule, "First-Come-First-Serve Scheduling", metrics_df)


def sjf_non_preemptive(processes):
    """Shortest Job First Scheduling (Non-Preemptive)."""
    processes = sorted(
        enumerate(processes), key=lambda x: x[1][0]
    )  # Sort by arrival time
    ready_queue = []
    current_time = 0
    schedule = []
    completion_times = [0] * len(processes)

    while processes or ready_queue:
        while processes and processes[0][1][0] <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: x[1][1])  # Sort by burst time
            idx, (arrival, burst) = ready_queue.pop(0)
            start_time = current_time
            current_time += burst
            completion_times[idx] = current_time
            schedule.append((idx + 1, start_time, current_time))
        else:
            current_time += 1

    metrics_df = calculate_metrics(
        [p[1] for p in sorted(enumerate(processes), key=lambda x: x[0])],
        completion_times,
    )
    gantt_chart_with_table(schedule, "Shortest Job First Scheduling", metrics_df)


def priority_non_preemptive(processes):
    """Priority Scheduling (Non-Preemptive)."""
    processes = sorted(
        enumerate(processes), key=lambda x: x[1][0]
    )  # Sort by arrival time
    ready_queue = []
    current_time = 0
    schedule = []
    completion_times = [0] * len(processes)

    while processes or ready_queue:
        while processes and processes[0][1][0] <= current_time:
            ready_queue.append(processes.pop(0))
        if ready_queue:
            ready_queue.sort(key=lambda x: x[1][2])  # Sort by priority
            idx, (arrival, burst, priority) = ready_queue.pop(0)
            start_time = current_time
            current_time += burst
            completion_times[idx] = current_time
            schedule.append((idx + 1, start_time, current_time))
        else:
            current_time += 1

    metrics_df = calculate_metrics(
        [p[1] for p in sorted(enumerate(processes), key=lambda x: x[0])],
        completion_times,
    )
    gantt_chart_with_table(schedule, "Priority Scheduling (Non-Preemptive)", metrics_df)


def round_robin(processes, quantum):
    """Round Robin Scheduling (Preemptive)."""
    queue = []
    schedule = []
    n = len(processes)
    burst_times = [p[1] for p in processes]
    remaining_times = burst_times[:]
    arrival_times = [p[0] for p in processes]
    current_time = 0
    waiting_times = [0] * n
    turnaround_times = [0] * n
    visited = [False] * n

    while True:
        for i in range(n):
            if (
                arrival_times[i] <= current_time
                and remaining_times[i] > 0
                and not visited[i]
            ):
                queue.append(i)
                visited[i] = True

        if not queue:
            current_time += 1
            continue

        i = queue.pop(0)
        if remaining_times[i] > quantum:
            schedule.append((i + 1, current_time, current_time + quantum))
            current_time += quantum
            remaining_times[i] -= quantum
        else:
            schedule.append((i + 1, current_time, current_time + remaining_times[i]))
            current_time += remaining_times[i]
            remaining_times[i] = 0

        if remaining_times[i] > 0:
            queue.append(i)

        if sum(remaining_times) == 0:
            break

    metrics_df = calculate_metrics(processes, [s[2] for s in schedule])
    gantt_chart_with_table(schedule, "Round Robin Scheduling", metrics_df)


def main():
    while True:
        print("\nCPU Scheduling Algorithms")
        print("1. First-Come-First-Serve (FCFS)")
        print("2. Shortest Job First (Non-Preemptive)")
        print("3. Priority Scheduling (Non-Preemptive)")
        print("4. Round Robin (Preemptive)")
        print("5. Exit")

        choice = int(input("Enter your choice: "))

        if choice in [1, 2, 3]:
            n = int(input("Enter number of processes: "))
            processes = []
            for i in range(n):
                arrival = int(input(f"Enter arrival time for Process {i + 1}: "))
                burst = int(input(f"Enter burst time for Process {i + 1}: "))
                priority = None
                if choice == 3:
                    priority = int(input(f"Enter priority for Process {i + 1}: "))
                processes.append(
                    (arrival, burst) if choice != 3 else (arrival, burst, priority)
                )

            if choice == 1:
                fcfs(processes)
            elif choice == 2:
                sjf_non_preemptive(processes)
            elif choice == 3:
                priority_non_preemptive(processes)
        elif choice == 4:
            n = int(input("Enter number of processes: "))
            processes = []
            for i in range(n):
                arrival = int(input(f"Enter arrival time for Process {i + 1}: "))
                burst = int(input(f"Enter burst time for Process {i + 1}: "))
                processes.append((arrival, burst))

            quantum = int(input("Enter time quantum: "))
            round_robin(processes, quantum)
        elif choice == 5:
            break


if __name__ == "__main__":
    main()
