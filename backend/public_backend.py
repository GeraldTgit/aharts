from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from fpdf import FPDF
import subprocess
import traceback
import tempfile
import datetime
import getpass
import psutil
import shutil
import ctypes
import sys
import csv
import os

from functools import lru_cache

# May main header / Application name
my_main_header = "⎾Anthony's Home Appliance-Repair Ticketing System⏌"

# present working directory
@lru_cache(maxsize=None)
def pwd_():
    return os.getcwd().replace('\\','/')+"/"

# PARAMETERS
# Parameter directory
param_dir = pwd_()+'param/'

# Icons/logo directory
icons_dir = pwd_()+'icons/'

# id_type_list icon absolute path
id_type_list_dir = param_dir+'id_type.txt'

# tsystem log directory
logs_dir = pwd_()+"system_logs/"

# DATABASES
# temporary directory path
temp_db_dir =  pwd_()+"temp_db/"

# id directory
id_db_dir = temp_db_dir+"id/"

# Receipt directory
receipt_db_dir = temp_db_dir+"receipt/"

# customer database absolute path
customer_db_dir = temp_db_dir+"customer.parquet"

# service ticket database absolute path
service_ticket_db_dir = temp_db_dir+"service_ticket.parquet"

# troubleshooting order
troubleshooting_order_db_dir = temp_db_dir+"troubleshooting_order.parquet"

# BEAUTIFICATIONS
# id_type list absolute path
tsystem_icon = icons_dir+"tsystem.ico"

splash_gif = icons_dir+"splash_screen.gif"

# Task bar icon
myappid = 'tsystem.aharts.ticketingsystem.1'  # Replace with a unique identifier

# Dash line style
dash_line_style = "border: none; border-bottom: 1px dashed black;"

# Default error message
default_err_msg = "Something went wrong. Please contact the developer"

# DATABASE HEADERS

# Customer Database Column Headers
cust_db_headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email Address', 'Home Address', 'Presented ID', 'Identification']


# Service-Ticket database header
service_ticket_db_headers = ['Service-Ticket ID', 'Customer ID', 'Appliance', 'Brand', 'Model', 'Issue', 'Status']

#Troubleshooting Order table widget and db headers
table_widget_headers = ["Service", "Component", "Quantity", "Price", "Subtotal"]
ts_order_db_headers = ["Order ID","Service-Ticket ID", "Customer ID"] + table_widget_headers


########################################################
# FUNCTIONS
########################################################
#Look up Customer ID second column based on Service-Ticket ID first column
def look_up_cust_tracking_id(service_ticket_id):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(service_ticket_db_dir)

    # Search for the customer information
    row = df[df['Service-Ticket ID'] == service_ticket_id]
    if not row.empty:
        return row.iloc[0]['Customer ID']
    else:
        return None

def look_up_appliance(service_ticket_id):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(service_ticket_db_dir)

    # Search for the customer information
    row = df[df['Service-Ticket ID'] == service_ticket_id]
    if not row.empty:
        return f"{row.iloc[0]['Appliance']} [{row.iloc[0]['Brand']} {row.iloc[0]['Model']}]"
    else:
        return "No Service-Ticket Found"        
    
def look_up_issue(service_ticket_id):
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(service_ticket_db_dir)

    # Search for the customer information
    row = df[df['Service-Ticket ID'] == service_ticket_id]
    if not row.empty:
        return f"{row.iloc[0]['Issue']}"
    else:
        return "No Service-Ticket Found"        
    

def look_up_cust_name(customer_tracking_id): 
    # Read the Parquet file into a DataFrame
    df = pd.read_parquet(customer_db_dir)

    # Search for the customer information
    row = df[df['Customer ID'] == customer_tracking_id]
    if not row.empty:
        return f"{row.iloc[0]['First Name']} {row.iloc[0]['Last Name']}"
    else:
        return "No Information Found"


# Validate if widget is numerical only return integer
def validate_num_text(widget):
    text = widget.text()
    new_text = "".join(char for char in text if char.isdigit() or char == ".")
    widget.setText(new_text)
    try:
        return int(new_text)
    except:
        pass
