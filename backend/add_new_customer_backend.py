# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
from database_viewer import *
from backend.public_backend import *
from backend.logs_generator import *

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

    destination_folder = id_db_dir
                    
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
        log_message(f"Identification uploaded: {new_file_name}")
        return new_file_name.replace(' ','_') 
    except:
        pass


# Save new customer information
def save_new(customer_info):

    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(customer_db_dir)

    if len(df) > 0:
        if 0 in df['Customer ID'].values:
            # Customer ID already exists, do nothing
            return

    # Assign a new Customer ID
    highest_cust_id = df['Customer ID'].max() if not df.empty else 0
    new_entry_cust_id = highest_cust_id + 1

    # Add the new customer entry to the DataFrame
    customer_info.insert(0, new_entry_cust_id)
    new_entry = pd.DataFrame([customer_info], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)

    # Write the updated DataFrame back to the Parquet file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    df.to_parquet(temp_file.name)

    # Replace the original file with the updated file
    shutil.move(temp_file.name, customer_db_dir)

    # Prompt message and log
    message = f"New customer added: {customer_info}"
    QMessageBox.information(None, "AHARTS", message)
    log_message(message)

    return new_entry_cust_id
