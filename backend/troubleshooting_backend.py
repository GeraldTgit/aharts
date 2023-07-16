from backend.public_backend import *
from backend.logs_generator import *


# Troubleshooting order types
def services():
    return ['REPAIR ONLY/LABOR', 'REPLACED BROKEN PARTS']


###################################################################################################################################

def check_troubleshooting_order_db():
    if not os.path.isfile(troubleshooting_order_db_dir):
        # Create a new service ticket.parquet file with service_ticket_db_headers
        df = pd.DataFrame(columns=ts_order_db_headers)
        df.to_parquet(troubleshooting_order_db_dir)
        log_message('Troubleshooting Order database created.')

###################################################################################################################################

def generate_order_id(table_widget):
    # Read existing data from the Parquet file into a DataFrame
    df = pd.read_parquet(troubleshooting_order_db_dir)

    if len(df) > 0:
        # Get the max value from the 'Order ID' column or assign 0 if the DataFrame is empty
        highest_order_id = int(df['Order ID'].max())
    else:
        highest_order_id = 0

    try:
        # Check highest Order ID in table_widget which is in the first column
        table_order_ids = [int(table_widget.item(row, 0).text()) for row in range(table_widget.rowCount())]
    except:
        QMessageBox.information(None, 'AHARTS', 'Please try again')

    highest_table_order_id = max(table_order_ids) if table_order_ids else None

    if highest_table_order_id is None and highest_order_id == 0:
        highest_order_id = 1
    elif highest_table_order_id is None and highest_order_id is not None:
        highest_order_id += 1
    else:
        highest_order_id = max(highest_order_id, highest_table_order_id) + 1

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
    return f'Php {grand_total}'

###################################################################################################################################

def save_ts_order(table_widget, service_ticket_id, customer_id):
    check_troubleshooting_order_db()

    # Read data from QTableWidget
    table_data = []

    for row in range(table_widget.rowCount()):
        row_data = []
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            row_data.append(item.text())
        table_data.append(row_data)
        
    
    # Insert Service-Ticket ID and Customer ID in table_data
    for row in table_data:
        row.insert(1, service_ticket_id)
        row.insert(2, customer_id)


    # Read and filter parquet data based on Service-Ticket ID
    parquet_data = pd.read_parquet(troubleshooting_order_db_dir)
    filtered_data = parquet_data[parquet_data['Service-Ticket ID'].isin([int(row[1]) for row in table_data])]

    # Convert Order ID, Service-Ticket ID, and Customer ID to integers
    filtered_data['Order ID'] = filtered_data['Order ID'].astype(int)
    filtered_data['Service-Ticket ID'] = filtered_data['Service-Ticket ID'].astype(int)
    filtered_data['Customer ID'] = filtered_data['Customer ID'].astype(int)

    # Update or append data in the parquet file
    for row in table_data:
        order_id = int(row[0])
        if order_id in filtered_data['Order ID'].values:

            # Update data from table_data to filtered_data
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Service-Ticket ID'] = int(row[1])
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Customer ID'] = int(row[2])
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Service'] = row[3]
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Broken Component'] = row[4]
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Quantity'] = row[5]
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Price'] = row[6]
            filtered_data.loc[filtered_data['Order ID'] == order_id, 'Subtotal'] = row[7]

            # Prompt message and log
            message = f"An Order has been updated: {[row[i] for i in range(8)]}"
            log_message(message)
            QMessageBox.information(None, "AHARTS", message)

        else:
            # Append new data to filtered_data
            print('Append new data to filtered_data')
            new_row = pd.DataFrame(
                [[int(row[0]), int(row[1]), int(row[2]), row[3], row[4], row[5], row[6], row[7]]],
                columns=['Order ID', 'Service-Ticket ID', 'Customer ID', 'Service', 'Broken Component', 'Quantity',
                        'Price', 'Subtotal'])
            # Append other columns from table_data if needed
            filtered_data = pd.concat([filtered_data, new_row], ignore_index=True)

            message = f"New Order added: {[row[i] for i in range(8)]}"
            log_message(message)
            QMessageBox.information(None, "AHARTS", message)

    # Save the updated parquet data back to the file
    updated_data = pd.concat([parquet_data, filtered_data], ignore_index=True)
    updated_data.drop_duplicates(subset='Order ID', keep='last', inplace=True)
    updated_data.to_parquet(troubleshooting_order_db_dir, index=False)


###################################################################################################################################

def look_up_ts_order_data(service_ticket_id):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(troubleshooting_order_db_dir)

    # Filter rows based on service_ticket_id
    data_rows = df[df['Service-Ticket ID'] == service_ticket_id]

    # Get the order details
    data_rows = data_rows[['Order ID'] + list(data_rows.columns[3:])]

    return data_rows
