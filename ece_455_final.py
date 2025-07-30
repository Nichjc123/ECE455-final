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

# Execute available tasks from start_time to end_time
def execute_tasks(start_time, end_time):
    global running_tasks, preemptions, currently_running_task, schedulable
    current_time = start_time
    time_gap = end_time - start_time

    while time_gap > 0 and running_tasks:
        running_tasks.sort(key=lambda x: x[2]) # Sort by deadline
        task_idx, remaining, deadline = running_tasks[0]

        # Check if we've missed this task's deadline
        if current_time >= deadline:
            schedulable = False
            return

        # Count preemption if switching to a new task
        if currently_running_task != -1 and currently_running_task != task_idx:
            preemptions[currently_running_task] += 1

        currently_running_task = task_idx

        # Determine execution time for this step
        exec_time = min(time_gap, remaining)
        current_time += exec_time
        time_gap -= exec_time

        if remaining <= exec_time:
            # Task completes
            running_tasks.pop(0)
            currently_running_task = -1
        else:
            running_tasks[0][1] -= exec_time
        
# Release tasks that are due at this time
def release_new_tasks(time):
    global running_tasks
    for i, (e, p, d) in enumerate(task_set):
        if time % p == 0:
            running_tasks.append([i, e, time + d])

def main():
    global task_set, release_times, preemptions, schedulable
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
        current_release = release_times[i]
        next_release = release_times[i + 1] if i + 1 < len(release_times) else hyperperiod

        release_new_tasks(current_release)

        execute_tasks(current_release, next_release)

        for _, _, deadline in running_tasks:
            if current_release > deadline:
                break

        # Check if any tasks could have been executed since last release time
            # if so, sort tasks by deadline and pick smallest to scheduler
            # update preemption list
            # update our global state
            # check to see if exceeded deadline during execution
            # continue until we have reached next release time
        
        # add any tasks to global state that should be released at this time

    # Print results
    if not schedulable:
        print(0)
        print()
    else:
        print(1)
        print(','.join(map(str, preemptions)))


if __name__ == "__main__":
    main()