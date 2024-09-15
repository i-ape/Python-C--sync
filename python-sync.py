import os
import time
import shutil
import logging
import sys

# Set up logging
def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')

# Log a message to both the console and log file
def log_message(message):
    logging.info(message)
    print(message)

# Sync function to copy files and remove deleted ones
def sync_folders(source, replica):
    log_message(f"Starting synchronization from {source} to {replica}")

    # Copy all files from source to replica
    for root, dirs, files in os.walk(source):
        for file in files:
            src_file = os.path.join(root, file)
            relative_path = os.path.relpath(src_file, source)
            dest_file = os.path.join(replica, relative_path)

            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            # Copy file if it doesn't exist or is different
            if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)
                log_message(f"Copied {src_file} to {dest_file}")

    # Remove files in replica that no longer exist in source
    for root, dirs, files in os.walk(replica):
        for file in files:
            replica_file = os.path.join(root, file)
            relative_path = os.path.relpath(replica_file, replica)
            source_file = os.path.join(source, relative_path)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                log_message(f"Deleted {replica_file} from replica")

    log_message("Synchronization completed.")

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python sync.py <source_folder> <replica_folder> <interval_in_seconds> <log_file>")
        sys.exit(1)

    source_folder = sys.argv[1]
    replica_folder = sys.argv[2]
    interval = int(sys.argv[3])
    log_file = sys.argv[4]

    # Set up logging
    setup_logging(log_file)

    # Run sync periodically
    while True:
        sync_folders(source_folder, replica_folder)
        time.sleep(interval)
