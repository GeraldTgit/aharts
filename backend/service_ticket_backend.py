from backend.public_backend import *
from backend.logs_generator import *

# Types of Appliances
def appliances():
    with open(param_dir+'appliances.txt', 'r') as file:
        appliances = file.readlines()

    return appliances

# Service status
def service_status():
    with open(param_dir+'service_status.txt', 'r') as file:
        service_status = file.readlines()

    return service_status


def save_new_ticket(service_info):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(service_ticket_db_dir)

    if len(df) > 0:
        if 0 in df['Service-Ticket ID'].values:
            # Service-Ticket ID already exists, do nothing
            return

    # Convert the 'Service-Ticket ID' column to integer type
    df['Service-Ticket ID'] = df['Service-Ticket ID'].astype(int)

    # Assign a new Service-Ticket ID
    highest_ticket_id = df['Service-Ticket ID'].max() if not df.empty else 0
    new_entry_ticket_id = highest_ticket_id + 1

    service_info.insert(0, new_entry_ticket_id)

    # Create a new DataFrame with the new service ticket entry
    new_entry = pd.DataFrame([service_info], columns=df.columns)

    # Concatenate the new entry with the existing DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)

    # Write the updated DataFrame back to the Parquet file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    df.to_parquet(temp_file.name)

    # Replace the original file with the updated file
    shutil.move(temp_file.name, service_ticket_db_dir)

    # Prompt message and log
    message = f"New service ticket created: {service_info}"
    QMessageBox.information(None, "AHARTS", message)
    log_message(message)

    return new_entry_ticket_id


