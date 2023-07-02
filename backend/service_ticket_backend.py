from PyQt5.QtWidgets import QMessageBox
import os
import csv
import tempfile
import shutil
import pyperclip

from backend.public_backend import *
from backend.logs_generator import *

# Types of Appliances
def appliances():
    with open(pwd_()+'/param/appliances.txt', 'r') as file:
        appliances = file.readlines()

    return appliances


# Service-Ticket database header
headers = ['Service-Ticket ID', 'Customer ID', 'Type of Appliance', 'Brand', 'Model', 'Issue']

def check_serv_ticket_db():
    if not os.path.isfile(service_ticket_db()):
        # Create a new service ticket CSV file with headers
        with open(service_ticket_db(), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            log_message("Service-Ticket database created.")

def save_new_ticket(service_info):
    check_serv_ticket_db()    
    # Assigning customer tracking number
    with open(service_ticket_db(), 'r') as file:
        reader = csv.reader(file)
        # skip header row if it exists
        if csv.Sniffer().has_header(file.read(1024)):
            file.seek(0)
            next(reader)

        try:
            # Get the max value from the first column or assign 0 if the reader is empty
            highest_ticket_id = max(int(row[0]) for row in reader)
        except ValueError:
            highest_ticket_id = 0

    # Assign a value of 1 if no existing entries
    new_entry_ticket_id = highest_ticket_id + 1
    pyperclip.copy(new_entry_ticket_id)

    # Concatenate service information
    service_info.insert(0,new_entry_ticket_id)
    
    # Rest of the code to update or append rows
    with open(service_ticket_db(), 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
        if len(rows) > 0:
            for row in rows:
                if row[0] == 0:
                    # Service-Ticket ID already exists, do nothing
                    break
            else:
                # Service-Ticket ID doesn't exist, append a new row
                rows.append([info for info in service_info])
        else:
            # Service-Ticket.csv is empty, add the headers and append a new row
            rows.append(headers)
            rows.append([info for info in service_info])

    # Write the modified data back to the file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        with open(temp_file.name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)  # Write the rows

    # Replace the original file with the updated file
    shutil.move(temp_file.name, service_ticket_db())
    
    # Prompt message and log
    message = f"New service ticket created : {service_info}"
    QMessageBox.information(None, "AHARTS", message)        
    log_message(message)
