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
        running_tasks.sort(key=lambda x: (x[2], task_set[x[0]][2], x[0])) # Sort by deadline
        task_idx, remaining, deadline = running_tasks[0]

        # Check if we've missed this task's deadline
        if current_time >= deadline:
            schedulable = False
            return

        # Count preemption if switching to a new task
        if currently_running_task != -1 and currently_running_task != task_idx:
            preemptions[currently_running_task] += 1

        currently_running_task = task_idx

        #print(f"ran task {task_idx} for {min(time_gap, remaining)} time units. Current time is: {current_time}")

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
        
        #print(running_tasks)

        # Check if task misses its deadline after running
        if current_time > deadline:
            schedulable = False
            return
        
# Release tasks that are due at this time
def release_new_tasks(time):
    global running_tasks
    #print(f"Adding tasks at time '{time}")
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
                curr_task = tuple(map(float, line.strip().split(',')))
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
    #print(release_times)

    for i in range(len(release_times) - 1):
        current_release = release_times[i]
        next_release = release_times[i + 1] if i + 1 < len(release_times) else hyperperiod

        release_new_tasks(current_release)

        execute_tasks(current_release, next_release)

        if not schedulable:
            break

    # Final deadline check for remaining tasks
    if running_tasks:
        schedulable = False

    # Print results
    if not schedulable:
        print(0)
        print()
    else:
        print(1)
        print(','.join(map(str, preemptions)))


if __name__ == "__main__":
    main()