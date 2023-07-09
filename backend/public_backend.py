from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess
import pyperclip
import traceback
import pyperclip
import tempfile
import datetime
import psutil
import shutil
import ctypes
import sys
import csv
import os

# present working directory
def pwd_():
    return os.getcwd().replace('\\','/')+"/"

# PARAMETERS
# Parameter directory
def param():
    return pwd_()+'param/'

# id_type_list icon absolute path
def id_type_list():
    return param()+'id_type.txt'

# DATABASES
# temporary directory path
def temp_db():
    return pwd_()+"temp_db/"

# customer database absolute path
def customer_db():
    return temp_db()+"customer.csv"

# service ticket database absolute path
def service_ticket_db():
    return temp_db()+"service_ticket.csv"

# troubleshooting order
def troubleshooting_order_db():
    return temp_db()+"troubleshooting_order.csv"


# BEAUTIFICATIONS
# id_type list absolute path
def tsystem_icon():
    return pwd_()+"tsystem.ico"

# Task bar icon
def myappid():
    return 'tsystem.aharts.ticketingsystem.1'  # Replace with a unique identifier

########################################################
# FUNCTIONS
########################################################

# If copied to clipboard is numeric return, else do nothing
def if_valid_txn_number(in_clipboard):
    if in_clipboard.isnumeric() == True:
        return in_clipboard
    

def look_up_cust_tracking_id(service_ticket_id):
    # Open the CSV file and search for the customer information
    with open(service_ticket_db(), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if service_ticket_id in row:
                return row[1]
                break
        else:
            return None

def look_up_appliance(service_ticket_id):
    # Open the CSV file and search for the customer information
    with open(service_ticket_db(), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if service_ticket_id in row:
                return row[2]
                break
        else:
            return "No Service-Ticket Found"        

def look_up_cust_name(customer_tracking_id):
    # Open the CSV file and search for the customer information
    with open(customer_db(), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if customer_tracking_id in row:
                return f"{row[1]} {row[2]}"
                break
        else:
            return "No Information Found"


def look_up_ts_order_data(service_ticket_id):
    # Load Troubleshooting order base on service_ticket_id
    with open(troubleshooting_order_db(), 'r') as file:
        reader = csv.reader(file)
        # Append order id to the rest of order details
        data_rows = [[row[0]]+row[3:] for row in reader if row and row[1] == service_ticket_id]
        return data_rows
