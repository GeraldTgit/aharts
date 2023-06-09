import datetime
import os

# Setting directory
pwd_ = os.getcwd().replace('\\', '/')
logs_dir = pwd_ + "/temp_db/logs/"

# Generate the new filename with the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Generate timestamping for each log
current_time = datetime.datetime.now().strftime("%H:%M:%S")

# log file path + new file name
logs_absolute_dir = logs_dir + "aharts_log_" + current_date + ".log"

def setup_log_file():
    # Check if the directory exists, and create it if necessary
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Check if the file exists, and create it if necessary
    if not os.path.exists(logs_absolute_dir):
        with open(logs_absolute_dir, 'w') as file:
            file.write(f"{current_time} : Log file created" + "\n")

# Open the file in append mode and write the log message
def log_message(message):
    with open(logs_absolute_dir, 'a') as file:
        file.write(f"{current_time} : {message}" + "\n")
