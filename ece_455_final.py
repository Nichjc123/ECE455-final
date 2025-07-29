import sys

def main():
    #HANDLE FILE INPUT
    filename = sys.argv[1]

    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    
if __name__ == "__main__":
    main()