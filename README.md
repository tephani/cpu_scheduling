# CPU Scheduling Algorithms

This program simulates and visualizes various CPU scheduling algorithms: **First-Come-First-Serve (FCFS)**, **Shortest Job First (SJF)**, **Priority Scheduling**, and **Round Robin (RR)**. It calculates key scheduling metrics like **Turnaround Time (TAT)** and **Waiting Time (WT)** and displays the results in a table along with a Gantt Chart visualization.

## Features

- **First-Come-First-Serve (FCFS)**: A non-preemptive scheduling algorithm where processes are executed in the order they arrive.
- **Shortest Job First (SJF)**: A non-preemptive scheduling algorithm where processes with the shortest burst time are executed first.
- **Priority Scheduling**: A non-preemptive scheduling algorithm where processes with the highest priority are executed first.
- **Round Robin (RR)**: A preemptive scheduling algorithm that assigns a fixed time quantum to each process.

## Prerequisites

To run the program, you need Python installed along with the following dependencies:
- `matplotlib` for Gantt chart visualization
- `pandas` for tabular display of results

You can install these libraries using `pip`:

```bash
pip install matplotlib pandas
```

## Running the Program
1. Clone or download the repository to your local machine.
2. Navigate to the project directory and open a terminal or command prompt.
3. Run the program using the following command:

```
python cpu_scheduling.py
```

## Program Flow
1. The program will display a menu with the following options:

- 1: First-Come-First-Serve (FCFS)
- 2: Shortest Job First (SJF)
- 3: Priority Scheduling
- 4: Round Robin (RR)
- 5: Exit

2. Choose the desired scheduling algorithm by entering the corresponding number.

3. For the selected algorithm, input the number of processes and their respective arrival times and burst times (and priority for Priority Scheduling).

4. If you select Round Robin, you will also need to input a time quantum.

5. After inputting the data, the program will calculate the Turnaround Time (TAT) and Waiting Time (WT) for each process, then display the results in a table format along with a Gantt chart.

6. The program will also display the average Turnaround Time and average Waiting Time for all processes.

