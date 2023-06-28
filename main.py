# Anthony's Home Appliance Repair Ticketing System
# Common packages
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import datetime
import ctypes
import sys

# Customize scripts
# Sub-pages
from aharts_cust_form import AddNew_CustWindow
from aharts_edit_customer import Edit_CustWindow

# Backend scripts
from logs_generator import *
from add_new_customer_backend import *
from goto_page import *
from public_backend import *


# Param checker
setup_log_file()
check_customer_db()

current_time = datetime.datetime.now()
current_hour = current_time.hour

# Task bar icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid())

if current_hour < 12:
    greetings = "Good morning!"
elif 12 <= current_hour < 18:
    greetings = "Good afternoon!"
else:
    greetings = "Good evening!"

current_date = current_time.strftime("%A, %B %d, %Y")

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AHARTS - Main Menu")
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(QIcon(tsys_icon()))

        # Userform header
        uf_header = QLabel("Anthony's Home Appliance-Repair Ticketing System")
        uf_header.setFont(QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform greeting
        uf_greet_header = QLabel(greetings)
        uf_greet_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(uf_greet_header)

        # Show date today
        label_today = QLabel(f"Today is {current_date}")
        label_today.setFont(QFont('Arial', 9))
        self.layout().addWidget(label_today, alignment=Qt.AlignTop | Qt.AlignRight)

        # create a QLabel object to display the time
        self.uf_current_time = QLabel(self)
        self.uf_current_time.setFont(QFont('Arial', 9))
        self.layout().addWidget(self.uf_current_time, alignment=Qt.AlignTop | Qt.AlignRight)

        # start the timer to update the label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # update every 1 second

        # Customer form header
        cust_header = QLabel("Customer Form")
        cust_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header)


        #########################################################################
        # BUTTONS
        #########################################################################

        # Create a button to open the other user form
        cust_entry_button = QPushButton("Add New Customer", clicked = lambda: self.open_addnew_custwindow())
        self.layout().addWidget(cust_entry_button)

        # call aharts_edit_customer.py
        cust_edit_button = QPushButton("Edit Customer Information", clicked = lambda: self.open_edit_custwindow())
        self.layout().addWidget(cust_edit_button)

        # Ticket form header
        cust_header = QLabel("Ticket Form")
        cust_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_ticket_entry.py
        ticket_entry_button = QPushButton("Service Ticket", clicked = lambda: goto_page("create_service_ticket.py"))
        self.layout().addWidget(ticket_entry_button)

        # Appliance troubleshooting log
        appliance_ts_log = QPushButton("Appliance Troubleshooting Log", clicked = lambda: goto_page("troubleshooting.py"))
        self.layout().addWidget(appliance_ts_log)

        # Databases
        cust_header_db = QLabel("Database")
        cust_header_db.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header_db)

        # Open database button
        cust_db_button = QPushButton("View Customer Database", clicked = lambda: goto_page("database_viewer.py"))
        self.layout().addWidget(cust_db_button)

        # refresh page
        reload_button = QPushButton("RELOAD PAGE", clicked = lambda: goto_page("main.py"))
        reload_button.setFont(QFont('Arial', 15))
        self.layout().addWidget(reload_button)

        
    ########################################################
    # FUNCTIONS
    ########################################################

    def open_addnew_custwindow(self):
        # Show the other user form and hide the main form
        # Create an instance of the other user form
        self.addnew_custwindow = AddNew_CustWindow()
        # Add the other user form to the layout of the main form
        self.layout().addLayout(self.addnew_custwindow.layout())
        self.addnew_custwindow.show()
        self.hide()

    def open_edit_custwindow(self):
        self.edit_custwindow = Edit_CustWindow()
        # Add the other user form to the layout of the main form
        self.layout().addLayout(self.edit_custwindow.layout())
        self.edit_custwindow.show()
        self.hide()

        
    # This code updates uf_current_time every seconds
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.uf_current_time.setText(current_time)

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())
