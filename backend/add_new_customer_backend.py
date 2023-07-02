# Anthony's Home Appliance Repair Ticketing System
from PyQt5.QtWidgets import QMessageBox
import tempfile
import datetime
import shutil
import os
import csv

# Customize scripts
from logs_generator import *
from add_new_customer_backend import *
from goto_page import *
from public_backend import *

# SETUP EVERYTHING FIRST

# Customer database header
headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Home Address', 'ID Type', 'ID Path']

def upload_identification(id_path):
    # Slicing identification label to get the id absolute path only
    # Find the index of '=' and '>'
    start_index = id_path.find('=')
    end_index = id_path.find('>')
    # Extract the substring between '=' and '>'
    id_path = id_path[start_index + 1 : end_index]
    id_path=id_path.replace('"','')

    # assigning default value if no id is provided
    if id_path == "Identification":
        return "No Idenfication provided."

    destination_folder = temp_db()+"id/"
                    
    # Get the filename and extension from the source path
    file_name = os.path.basename(id_path)
    file_name, file_extension = os.path.splitext(file_name)

    # Generate the new filename with the current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name = f"{file_name}_{current_date}{file_extension}"

    # Create the destination path by combining the destination folder and the new filename
    destination_path = os.path.join(destination_folder, new_file_name)

    # Copy the file to the destination folder
    destination_path=destination_path.replace(' ','_')                   
    try:
        shutil.copy2(id_path, destination_path)
        log_message(f"Identification uploaded: {destination_path}")
        return destination_path
    except:
        pass

# Check if the customer.csv file exists in the customer_db() directory
def check_customer_db():
    if not os.path.isfile(customer_db()):
        # Create a new customer.csv file with headers
        with open(customer_db(), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            log_message("Customer database created.")

def save_new(customer_info):         
    # Assigning customer tracking number
    with open(customer_db(), 'r') as file:
        reader = csv.reader(file)
        # skip header row if it exists
        if csv.Sniffer().has_header(file.read(1024)):
            file.seek(0)
            next(reader)

        try:
            # Get the max value from the first column or assign 0 if the reader is empty
            highest_cust_id = max(int(row[0]) for row in reader)
        except ValueError:
            highest_cust_id = 0

    # Assign a value of 1 if no existing entries
    new_entry_cust_id = highest_cust_id + 1

    # Concatenate customer information
    customer_info.insert(0,new_entry_cust_id)
    
    # Rest of the code to update or append rows
    with open(customer_db(), 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        if len(rows) > 0:
            for row in rows:
                if row[0] == 0:
                    # Customer ID already exists, do nothing
                    break
            else:
                # Customer ID doesn't exist, append a new row
                rows.append([info for info in customer_info])
        else:
            # Customer.csv is empty, add the headers and append a new row
            rows.append(headers)
            rows.append([info for info in customer_info])

    # Write the modified data back to the file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        with open(temp_file.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)  # Write the rows

    # Replace the original file with the updated file
    shutil.move(temp_file.name, customer_db())
    
    # Prompt message and log
    message = f"New customer added : {customer_info}"
    QMessageBox.information(None, "AHARTS", message)        
    log_message(message)
