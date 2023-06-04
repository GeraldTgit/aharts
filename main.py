# Anthony's Home Appliance Repair Ticketing System
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import QTimer
import subprocess
import datetime
import sys
import os

current_time = datetime.datetime.now()
current_hour = current_time.hour

if current_hour < 12:
    greetings = "Good morning!"
elif 12 <= current_hour < 18:
    greetings = "Good afternoon!"
else:
    greetings = "Good evening!"

current_date = current_time.strftime("%A, %B %d, %Y")

# present working directory
pwd_ = os.getcwd()

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Menu Page")
        # Userform layout
        self.setLayout(qtw.QVBoxLayout())

        # Userform header
        uf_header = qtw.QLabel("Anthony's Home Appliance Repair Ticketing System")
        uf_header.setFont(qtg.QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform greeting with date
        uf_greet_header = qtw.QLabel(greetings + "                                                     Today is " + current_date)
        uf_greet_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(uf_greet_header)

        # create a QLabel object to display the time
        self.uf_current_time = qtw.QLabel(self)
        self.uf_current_time.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(self.uf_current_time)

        # start the timer to update the label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # update every 1 second

        # Customer form header
        cust_header = qtw.QLabel("Customer Form")
        cust_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_cust_form.py
        cust_entry_button = qtw.QPushButton("Add New Customer", clicked = lambda: cust_entry_form())
        self.layout().addWidget(cust_entry_button)

        # call aharts_edit_customer.py
        cust_edit_button = qtw.QPushButton("Edit Customer Information", clicked = lambda: aharts_edit_customer())
        self.layout().addWidget(cust_edit_button)

        # Ticket form header
        cust_header = qtw.QLabel("Ticket Form")
        cust_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_ticket_entry.py
        ticket_entry_button = qtw.QPushButton("Service Ticket", clicked = lambda: ticket_entry_form())
        self.layout().addWidget(ticket_entry_button)

        # Databases
        cust_header_db = qtw.QLabel("Database")
        cust_header_db.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(cust_header_db)

        # Open database button
        cust_db_button = qtw.QPushButton("View Customer Database", clicked = lambda: open_database_viewer())
        self.layout().addWidget(cust_db_button)

        # refresh page
        reload_button = qtw.QPushButton("RELOAD PAGE", clicked = lambda: reload())
        reload_button.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(reload_button)

        # This part is very IMPORTANT!!
        self.show()

        # To call customer form
        def cust_entry_form():
            CloseOpen("aharts_cust_form.py")

        # To call edit customer information form
        def aharts_edit_customer():
            CloseOpen("aharts_edit_customer.py")

        # To call ticket form
        def ticket_entry_form():
            print("Wala pa. Wag kang excited")


        # To open the customer database view form
        def open_database_viewer():
            # Path to the Python script you want to rerun
            script_path = pwd_+"/database_viewer.py"

            # Define the command to run the new script
            new_script_command = ["python", script_path]

            # Start the new script
            subprocess.Popen(new_script_command)

        # To reload the page
        def reload():
            CloseOpen("reload.py")

        # To close existing script and then open main.py
        def CloseOpen(page):
            # Path to the Python script you want to rerun
            script_path = pwd_+"/"+page
            # Define the command to run the new script
            new_script_command = ["python", script_path]
            # Start the new script
            subprocess.Popen(new_script_command)
            # Exit the current script
            sys.exit()
            

    # This code updates uf_current_time every seconds
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.uf_current_time.setText("                                                                                                                                                                                                                              " + current_time)

app = qtw.QApplication([])
mw = MainWindow()

app.exec_()

