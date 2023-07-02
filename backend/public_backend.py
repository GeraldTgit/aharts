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


# BEAUTIFICATIONS
# id_type list absolute path
def tsystem_icon():
    return pwd_()+"tsystem.ico"

# Task bar icon
def myappid():
    return 'tsystem.aharts.ticketingsystem.1'  # Replace with a unique identifier

