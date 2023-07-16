from backend.public_backend import *
from backend.logs_generator import *

# Parameter file checking
# Check if the customer.csv file exists in the customer_db_dir directory
def check_customer_db():
    if not os.path.isfile(customer_db_dir):
        # Create a new customer.parquet file with cust_db_headers
        df = pd.DataFrame(columns=cust_db_headers)
        df.to_parquet(customer_db_dir)     
        log_message("Customer database created.")

def check_serv_ticket_db():
    if not os.path.isfile(service_ticket_db_dir):
        # Create a new service ticket.parquet file with service_ticket_db_headers
        df = pd.DataFrame(columns=service_ticket_db_headers)
        df.to_parquet(service_ticket_db_dir)
        log_message("Service-Ticket database created.")

def check_troubleshooting_order_db():
    if not os.path.isfile(troubleshooting_order_db_dir):
        # Create a new service ticket.parquet file with service_ticket_db_headers
        df = pd.DataFrame(columns=ts_order_db_headers)
        df.to_parquet(troubleshooting_order_db_dir)
        log_message('Troubleshooting Order database created.')