# Download Organizer
import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the download folder and the destination folders for different file types
download_folder = r"C:\Users\<username>\Downloads"
# Change to desired destination paths
destination_folders = {
    "pdf": r"C:\Users\<username>\Desktop\PdfFolder",
    "jpg": r"C:\Users\<username>\Desktop\JpgFolder",
    "docx": r"C:\Users\<username>\Desktop\Docx"
}

# Counter for handling duplicate file names
file_counter = {}


# Function to get the destination folder based on the file extension
def move_file(file_path, destination_folder, file_extension):
    time.sleep(3)
    try:
        # Add file extension here
        if file_extension.lower() in ["pdf", "jpg", "docx"]:
            shutil.move(file_path, destination_folder)
            print(f"Moved {file_path} to {destination_folder}")
        else:
            print(f"Ignored {file_path}: File type not supported")
    except shutil.Error as e:
        if "already exists" in str(e):
            # Destination path already exists, rename the file with a file counter
            file_name = os.path.basename(file_path)
            if file_name in file_counter:
                file_counter[file_name] += 1
            else:
                file_counter[file_name] = 1
            # Append counter before file extension
            new_file_name = f"{os.path.splitext(file_name)[0]}_{file_counter[file_name]}.{file_extension}"
            new_file_path = os.path.join(destination_folder, new_file_name)
            shutil.move(file_path, new_file_path)
            print(f"Moved {file_path} to {new_file_path} (file already exists)")
        else:
            print(f"Error: {e}")
    except FileNotFoundError:
        print(f"Error: File not found or already moved: {file_path}")


# Function to get the destination folder based on the file extension
def get_destination_folder(file_extension):
    for category, folder_path in destination_folders.items():
        if file_extension.lower() in category.lower():
            return folder_path
    return download_folder  # Return the download folder if no specific category matches


# Event handler class to watch for file creation events
class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:  # Check if event is not a directory creation
            file_path = event.src_path
            if file_path.endswith('.part'):  # Ignore .part files
                return
            file_extension = os.path.splitext(file_path)[1][1:]  # Get the file extension
            destination_folder = get_destination_folder(file_extension)
            move_file(file_path, destination_folder, file_extension)  # Pass file_extension as an argument


# Function to start the watchdog observer
def start_observer():
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, download_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_observer()