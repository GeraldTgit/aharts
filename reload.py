import subprocess
import sys
import os

pwd_ = os.getcwd()

# Path to the Python script you want to rerun
script_path = pwd_+"/main.py"

# Define the command to run the new script
new_script_command = ["python", script_path]

# Start the new script
subprocess.Popen(new_script_command)

# Exit the current script
sys.exit()
