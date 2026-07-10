import os
import sys
import subprocess

def locate_and_run():
    # Ensure the user actually typed 'run .'
    args = sys.argv[1:]
    if len(args) < 2 or args[0] != "run" or args[1] != ".":
        print("Usage: py run .")
        sys.exit(1)

    # Find every file ending with .py in the current directory
    all_files = [f for f in os.listdir(".") if f.endswith(".py")]

    if all_files:
        # If there are multiple files, sort them so the most recently modified runs first
        if len(all_files) > 1:
            all_files.sort(key=os.path.getmtime, reverse=True)
            
        chosen_file = all_files[0]
        subprocess.run([sys.executable, chosen_file])
        return

    print("Error: No Python files found in the current directory.")
    sys.exit(1)
