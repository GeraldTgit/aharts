import subprocess
import sys
import os

# present working directory
pwd_ = os.getcwd()

# To close existing script and then open main.py
def goto_page(page):
    # Path to the Python script you want to rerun
    script_path = pwd_+"/"+page
    # Define the command to run the new script
    new_script_command = ["python", script_path]
    # Start the new script
    subprocess.Popen(new_script_command)

    # Exit the current script if not database viewer page
    if page != "database_viewer.py":
        sys.exit()
