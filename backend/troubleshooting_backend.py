from backend.public_backend import *
from backend.logs_generator import *


# Troubleshooting types
def services():
    return ["REPAIR ONLY/LABOR", "REPLACED BROKEN PARTS"]


# Check if the customer.csv file exists in the customer_db() directory
table_widget_headers = ["Service", "Broken Component", "Quantity", "Price", "Subtotal"]
headers = ["Order ID","Service-Ticket ID", "Customer ID"] + table_widget_headers

###################################################################################################################################

# Checks if troubleshooting order exist
def check_troubleshooting_order_db():
    if not os.path.isfile(troubleshooting_order_db()):
        # Create a new customer.csv file with headers
        with open(troubleshooting_order_db(), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)
            log_message("Troubleshooting Order database created.")

###################################################################################################################################

def generate_order_id(table_widget):
    # Read existing data from the file
    with open(troubleshooting_order_db(), 'r') as file:       
        reader = csv.reader(file)
        # skip header row if it exists
        if csv.Sniffer().has_header(file.read(1024)):
            file.seek(0)
            next(reader)

        try:
            # Get the max value from the first column or assign 0 if the reader is empty
            highest_order_id = max(int(row[0]) for row in reader)
        except ValueError:
            highest_order_id = 0

    # Check highest Order ID in table_widget which is in the first column
    try:
        table_order_ids = [int(table_widget.item(row, 0).text()) for row in range(table_widget.rowCount())]
    except:
        QMessageBox.information(None, "AHARTS", 'Please try again')

    highest_table_order_id = max(table_order_ids) if table_order_ids else None

    if highest_table_order_id is None and highest_order_id == 0:
        highest_order_id = 1
    elif highest_table_order_id is None and highest_order_id is not None:
        highest_order_id += 1
    else:
        highest_order_id = highest_table_order_id + 1

    return highest_order_id

###################################################################################################################################

# Compute Subtotal
def compute_subtotal(quantity,price):
    if quantity and price:
        return round(float(quantity) * float(price), 2)
    elif price:
        return round(float(price), 2)
    else:
        return 0.0     
    
###################################################################################################################################

# Compute Grand Total
def compute_grand_total(table_widget):
    grand_total = 0.0
    for row in range(table_widget.rowCount()):
        subtotal_item = table_widget.item(row, 5)
        if subtotal_item is not None:
            try:
                subtotal = float(subtotal_item.text())
            except:
                continue
            grand_total += subtotal
    # Display the grand total in the table
    return f"Grand Total: {grand_total}"

###################################################################################################################################

def save_ts_order(table_widget, service_ticket_id, cust_name):
    # Read existing data from the file
    rows = []
    with open(troubleshooting_order_db(), 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Get the order IDs from the table_widget
    table_order_ids = [table_widget.item(row, 0).text() for row in range(table_widget.rowCount())]

    # Remove rows that have matching service_ticket_id but not in the table_widget
    rows = [row for row in rows if row[1] != service_ticket_id or row[0] in table_order_ids]

    # Append new rows from the table_widget or modify existing rows with matching order_id and service_ticket_id
    for row in range(table_widget.rowCount()):
        row_data = []

        # Get the order ID from the table_widget
        order_id = table_widget.item(row, 0).text()

        # Append the order ID, service_ticket_id, and cust_name to the row_data
        row_data.append(order_id)
        row_data.append(service_ticket_id)
        row_data.append(cust_name)

        # Append the rest of the row data
        for column in range(1, table_widget.columnCount()):  # Skip the first column
            item = table_widget.item(row, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")  # Empty cell

        # Check if there is an existing row with the same order ID and service_ticket_id
        existing_row = None
        for i, existing_row_data in enumerate(rows):
            if existing_row_data[0] == order_id and existing_row_data[1] == service_ticket_id:
                existing_row = i
                break

        # Update or append the row data
        if existing_row is not None:
            rows[existing_row] = row_data  # Update the existing row
        else:
            rows.append(row_data)  # Append a new row

    # Write the modified data back to the file
    with open(troubleshooting_order_db(), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    # Removes duplicate rows that has the same Order ID and service_ticket_id
    remove_duplicate_rows()

    # Prompt message and log
    message = "Troubleshooting order updated"
    QMessageBox.information(None, "AHARTS", message)
    log_message(message)

###################################################################################################################################

# Removes duplicate rows that has the same Order ID and service_ticket_id
def remove_duplicate_rows():
    # Read existing data from the file
    rows = []
    with open(troubleshooting_order_db(), 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Create a dictionary to keep track of unique rows based on order_id and service_ticket_id
    unique_rows = {}

    # Iterate over the rows and store unique rows in the dictionary
    for i, row in enumerate(rows):
        if i == 0:  # Skip the first row (column headers)
            continue

        order_id = row[0]
        service_ticket_id = row[1]
        row_key = (order_id, service_ticket_id)
        if row_key not in unique_rows:
            unique_rows[row_key] = row

    # Write the unique rows back to the file
    with open(troubleshooting_order_db(), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(rows[0])  # Write the column headers
        writer.writerows(unique_rows.values())
