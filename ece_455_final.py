import sys
# Deadline monotonic scheduling: Assign the priority based on time to deadline

# Storing set of task tuples 
# (execution time, period, deadline)
task_set = []

def main():
    # Handling file input
    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            for line in file.readlines():
                # Create tuple of (e, p, d) and add to task set
                task_set.append(tuple(line.replace("\n", "").split(',')))
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


if __name__ == "__main__":
    main()