import sys
import numpy as np

# Storing set of task tuples 
# (execution time, period, deadline)
task_set = []

# (time) - we can know which task(s) it corresponds to by seing if its divisible by period
release_times = []

# index of current task on CPU
currently_running_task = -1

def main():
    # for calculating hyperperiod
    periods = []

    # Handling file input
    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            for line in file.readlines():
                # Create tuple of (e, p, d) and add to task set
                curr_task = tuple(map(int, line.strip().split(',')))
                task_set.append(curr_task)
                periods.append(int(curr_task[1]))
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

    # Create an array of scheduling points, not including task finishing (up to hyperperiod)
    hyperperiod = np.lcm.reduce(periods)

    # Find set of all release times
    points = set()
    for i in range(len(task_set)):
        curr = 0
        while (curr <= hyperperiod):
            if curr not in points:
                points.add(curr)
                release_times.append(curr)
            curr += task_set[i][1]
    
    release_times.sort()


if __name__ == "__main__":
    main()