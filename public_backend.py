import os

# present working directory
def pwd_():
    return os.getcwd().replace('\\','/')+"/"

# temporary directory path
def temp_db():
    return pwd_()+"temp_db/"

# customer database absolute path
def customer_db():
    return temp_db()+"customer.csv"

# service ticket database absolute path
def service_ticket_db():
    return temp_db()+"service_ticket.csv"

# tsystem icon absolute path
def tsys_icon():
    return pwd_()+"tsystem.ico"
