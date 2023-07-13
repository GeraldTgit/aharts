from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess
import traceback
import tempfile
import datetime
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

# customer database absolute path
customer_db_dir = temp_db_dir+"customer.csv"

# service ticket database absolute path
service_ticket_db_dir = temp_db_dir+"service_ticket.csv"

# troubleshooting order
troubleshooting_order_db_dir = temp_db_dir+"troubleshooting_order.csv"


# BEAUTIFICATIONS
# id_type list absolute path
tsystem_icon = pwd_()+"tsystem.ico"

# Task bar icon
myappid = 'tsystem.aharts.ticketingsystem.1'  # Replace with a unique identifier


########################################################
# FUNCTIONS
########################################################
    
def look_up_cust_tracking_id(service_ticket_id):
    # Open the CSV file and search for the customer information
    with open(service_ticket_db_dir, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if service_ticket_id in row:
                return row[1]
                break
        else:
            return None

@lru_cache(maxsize=None)
def look_up_appliance(service_ticket_id):
    # Open the CSV file and search for the customer information
    with open(service_ticket_db_dir, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if service_ticket_id in row:
                return row[2]
                break
        else:
            return "No Service-Ticket Found"        

@lru_cache(maxsize=None)
def look_up_cust_name(customer_tracking_id): 
    # Open the CSV file and search for the customer information
    with open(customer_db_dir, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if customer_tracking_id in row:
                return f"{row[1]} {row[2]}"
                break
        else:
            return "No Information Found"

@lru_cache(maxsize=None)
def look_up_ts_order_data(service_ticket_id):
    # Load Troubleshooting order base on service_ticket_id
    with open(troubleshooting_order_db_dir, 'r') as file:
        reader = csv.reader(file)
        # Append order id to the rest of order details
        data_rows = [[row[0]]+row[3:] for row in reader if row and row[1] == service_ticket_id]
        return data_rows
