import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hashlib import md5
import argparse
import time

# Set up logging
def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')

# Log a message to both the console and log file
def log_message(message):
    logging.info(message)
    print(message)

# Calculate the MD5 checksum of a file
def calculate_md5(file_path):
    hash_md5 = md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

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

            # Check MD5 hash of both files to see if copying is necessary
            if not os.path.exists(dest_file) or calculate_md5(src_file) != calculate_md5(dest_file):
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

# Event handler for folder changes
class SyncHandler(FileSystemEventHandler):
    def __init__(self, source, replica):
        self.source = source
        self.replica = replica

    def on_any_event(self, event):
        log_message(f"Change detected in {self.source}. Syncing...")
        sync_folders(self.source, self.replica)

# Main function
if __name__ == "__main__":
    # Using argparse for argument parsing
    parser = argparse.ArgumentParser(description="Folder synchronization script using watchdog.")
    parser.add_argument('source_folder', type=str, help='Path to the source folder.')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder.')
    parser.add_argument('log_file', type=str, help='Path to the log file.')

    # Parse the arguments
    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log_file)

    # Initial sync to ensure replica is up-to-date
    sync_folders(args.source_folder, args.replica_folder)

    # Set up the observer for monitoring changes in the source folder
    event_handler = SyncHandler(args.source_folder, args.replica_folder)
    observer = Observer()
    observer.schedule(event_handler, args.source_folder, recursive=True)

    # Start the observer
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
