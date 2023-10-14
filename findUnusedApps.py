import os
import time
from datetime import datetime, timedelta


def find_unused_executables(folder_path, days_threshold):
    unused_programs = []

    # Get the current time
    current_time = datetime.now()

    # Loop through the files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        # Get the file's last access time
        file_stat = os.stat(file_path)
        last_access_time = datetime.fromtimestamp(file_stat.st_atime)

        # Check if the file has been accessed within the threshold
        if current_time - last_access_time > timedelta(days=days_threshold):
            unused_programs.append(file_name)

    return unused_programs


# Example usage
if __name__ == "__main__":
    folder_path = "/usr/bin"
    days_threshold = (
        90  # Consider a program "unused" if it hasn't been accessed in 90 days
    )
    unused_programs = find_unused_executables(folder_path, days_threshold)

    if unused_programs:
        print("Unused programs:")
        for program in unused_programs:
            print(f"  - {program}")
    else:
        print("No unused programs found.")
