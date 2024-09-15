#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <source_folder> <replica_folder> <log_file>"
  exit 1
fi

SOURCE=$1
REPLICA=$2
LOGFILE=$3

# Function to log messages to both console and log file
log_message() {
  local message="$1"
  echo "$(date +'%Y-%m-%d %H:%M:%S') - $message" | tee -a "$LOGFILE"
}

# Function to perform folder synchronization
sync_folders() {
  log_message "Starting synchronization from $SOURCE to $REPLICA"
  
  # Use rsync to sync files from source to replica
  rsync -av --delete "$SOURCE" "$REPLICA" | tee -a "$LOGFILE"
  
  log_message "Synchronization completed."
}

# Perform the sync
sync_folders
