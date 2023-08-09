# Anthony's Home Appliance Repair Ticketing System
from backend.public_backend import *

# Customize scripts
from backend.logs_generator import *
from backend.add_new_customer_backend import *
from backend.goto_page import *

# SETUP EVERYTHING FIRST

def upload_identification(id_path,update):
    # Slicing identification label to get the id absolute path only
    # Find the index of '=' and '>'
    start_index = id_path.find('=')
    end_index = id_path.find('>')
    # Extract the substring between '=' and '>'
    id_path = id_path[start_index + 1 : end_index]
    id_path=id_path.replace('"','')

    # Get the filename and extension from the source path
    file_name = os.path.basename(id_path)
    file_name, file_extension = os.path.splitext(file_name)

    # Cancelling upload if id not updated
    if update == "no":
        file_name = file_name.replace(' ','_')
        return file_name+file_extension

    destination_folder = id_db_dir

    # Generate the new filename with the current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    new_file_name = f"{file_name}_{current_date}{file_extension}"

    # Create the destination path by combining the destination folder and the new filename
    destination_path = os.path.join(destination_folder, new_file_name)

    # Copy the file to the destination folder
    destination_path=destination_path.replace(' ','_')                   
    try:
        shutil.copy2(id_path, destination_path)
        log_message(f"Identification updated: {new_file_name}")
        return new_file_name
    except:
        pass


def look_up_cust_info(search_query):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(customer_db_dir)

    # Filter the DataFrame based on the search query
    rows = df[df['Customer ID'] == search_query]

    if not rows.empty:
        # Customer information found, retrieve the first row
        row = rows.iloc[0]

        cust_info = [row['First Name'], row['Last Name'], row['Contact Number'], row['Email Address'], row['Home Address'], row['Presented ID'], row['Identification']]
        return cust_info
    else:
        return []


# Save update
def save_update(customer_info):   
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(customer_db_dir)

    customer_id = int(customer_info[0])

    # Filter the DataFrame based on the customer ID
    rows = df[df['Customer ID'] == customer_id]

    if not rows.empty:
        # Customer ID already exists, update the row
        before_update_cust_info = rows.iloc[0].tolist()[:8]
        after_update_cust_info = customer_info[:8]
        df.loc[rows.index, 'First Name':'Identification'] = customer_info[1:9]
    else:
        # Customer ID does not exist, append a new row
        new_row = pd.DataFrame([customer_info], columns=df.columns)
        df = df.append(new_row, ignore_index=True)

    # Write the updated DataFrame back to the Parquet file
    df.to_parquet(customer_db_dir, index=False)

    # Prompt message and log
    message = f"Customer information updated:\nFROM: {before_update_cust_info}\nTO: {after_update_cust_info}"
    QMessageBox.information(None, "AHARTS", message)
    log_message(message)
