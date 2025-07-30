import sys
import numpy as np

#########################
# GLOBAL scheduler state
########################
running_tasks          = [] # (task index, remaining execution time, absolute deadline)
preemptions            = [] 
currently_running_task = -1
task_set               = [] # (execution time, period, deadline)
release_times          = [] 
schedulable            = True

def main():
    # for calculating hyperperiod
    periods  = []
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

    preemptions = [0] * len(task_set)

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

    for i in range(len(release_times)):
        # Check if any tasks could have been executed since last release time
            # if so, sort tasks by deadline and pick smallest to scheduler
            # update preemption list
            # update our global state
            # check to see if exceeded deadline during execution
            # continue until we have reached next release time
        
        # add any tasks to global state that should be released at this time


if __name__ == "__main__":
    main()