# Python-C--sync
“* **watchdog**: The script uses the `watchdog` library to monitor the source folder for changes. * **SyncHandler**: This class inherits from `FileSystemEventHandler` and triggers the `sync_folders` function whenever there is any file system event (create, modify, delete). * **sync\_folders**: Copies files from the source to the replica folder, ensuring the replica is an exact copy. * **Observer**: The `Observer` watches the source folder for changes and calls the event handler when something happens.”


