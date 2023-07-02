# Anthony's Home Appliance Repair Ticketing System
# Common packages
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import traceback
import subprocess
import datetime
import ctypes
import sys

# Customize scripts
# Sub-pages
from aharts_cust_form import AddNewCustWindow
from aharts_edit_customer import Edit_CustWindow
from create_service_ticket import ServiceTicketWindow
from troubleshooting import TroubleshootingWindow

# Backend scripts
from database_viewer import *
from backend.logs_generator import *
from backend.goto_page import *
from backend.public_backend import *

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
        self.setWindowIcon(QIcon(tsystem_icon()))

        # Userform header
        main_header = QLabel("Anthony's Home Appliance-Repair Ticketing System")
        main_header.setFont(QFont('Arial', 25))
        self.layout().addWidget(main_header)

        # Userform greeting
        greeting_header = QLabel(greetings)
        greeting_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(greeting_header)

        # Show date today
        label_today = QLabel(f"Today is {current_date}")
        label_today.setFont(QFont('Arial', 9))
        self.layout().addWidget(label_today, alignment=Qt.AlignTop | Qt.AlignRight)

        # create a QLabel object to display the time
        self.lbl_current_time = QLabel(self)
        self.lbl_current_time.setFont(QFont('Arial', 9))
        self.layout().addWidget(self.lbl_current_time, alignment=Qt.AlignTop | Qt.AlignRight)

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

        # create a QHBoxLayout to hold the buttons
        cust_buttons_layout = QHBoxLayout()

        # Create a button to open the other user form
        cust_entry_button = QPushButton("Add New Customer", clicked = lambda: self.open_addnew_custwindow())
        cust_buttons_layout.addWidget(cust_entry_button)

        # call aharts_edit_customer.py
        cust_edit_button = QPushButton("Edit Customer Information", clicked = lambda: self.open_edit_custwindow())
        cust_buttons_layout.addWidget(cust_edit_button)

        # add the buttons layout to the main layout
        self.layout().addLayout(cust_buttons_layout)

        # Ticket form header
        cust_header = QLabel("Ticket Form")
        cust_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_ticket_entry.py
        ticket_entry_button = QPushButton("Service Ticket", clicked = lambda: self.open_create_service_ticketwindow())
        self.layout().addWidget(ticket_entry_button)

        # Appliance troubleshooting log
        appliance_ts_log = QPushButton("Appliance Troubleshooting Log", clicked = lambda: self.open_troubleshootingwindow())
        self.layout().addWidget(appliance_ts_log)

        # Databases
        cust_header_db = QLabel("Database")
        cust_header_db.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header_db)

        # Open database button
        cust_db_btn = QPushButton("View Customer Database", clicked = lambda: open_cust_database_viewer(self))
        self.layout().addWidget(cust_db_btn)

        # Open database button
        serviceticket_db_btn = QPushButton("View Service-Ticket Database", clicked = lambda: open_serviceticket_database_viewer(self))
        self.layout().addWidget(serviceticket_db_btn)

        # refresh page
        reload_button = QPushButton("RELOAD PAGE", clicked = lambda: reload_main())
        reload_button.setFont(QFont('Arial', 15))
        self.layout().addWidget(reload_button)
        
        ########################################################
        # FUNCTIONS
        ########################################################
        def reload_main():
            # Close the existing main form by quitting the application
            app.quit()
            # Restart the application
            subprocess.Popen([sys.executable, __file__])

    def open_addnew_custwindow(self):
        # Show the customer form and hide the main form
        self.hide()
        addnew_custwindow = AddNewCustWindow(self)
        addnew_custwindow.show()

    def open_edit_custwindow(self):
        self.hide()
        self.edit_custwindow = Edit_CustWindow(self)
        self.edit_custwindow.show()
        
    def open_create_service_ticketwindow(self):
        self.hide()
        self.create_service_ticketwindow = ServiceTicketWindow(self)
        self.create_service_ticketwindow.show()
       
    def open_troubleshootingwindow(self):
        self.hide()
        self.troubleshootingwindow = TroubleshootingWindow(self)
        self.troubleshootingwindow.show()
                 
    # This code updates lbl_current_time every seconds  
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.lbl_current_time.setText(current_time)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Close Application",
            "Are you sure you want to close the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

try:

    # Main application
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        main_form = MainForm()
        main_form.show()
        sys.exit(app.exec_())

except Exception as e:
    # Log the exception message and traceback
    error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
    log_message(error_message)
