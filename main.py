# Anthony's Home Appliance Repair Ticketing System
# Common packages
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
import datetime

# Customize scripts
from logs_generator import *
from add_new_customer_backend import *
from goto_page import *
from public_backend import *

# Param checker
setup_log_file()
check_customer_db()

current_time = datetime.datetime.now()
current_hour = current_time.hour

if current_hour < 12:
    greetings = "Good morning!"
elif 12 <= current_hour < 18:
    greetings = "Good afternoon!"
else:
    greetings = "Good evening!"

current_date = current_time.strftime("%A, %B %d, %Y")

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Main Manu")
        # Userform layout
        self.setLayout(qtw.QVBoxLayout())
        self.setWindowIcon(qtg.QIcon(tsys_icon()))

        # Userform header
        uf_header = qtw.QLabel("Anthony's Home Appliance-Repair Ticketing System")
        uf_header.setFont(qtg.QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform greeting
        uf_greet_header = qtw.QLabel(greetings)
        uf_greet_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(uf_greet_header)

        # Show date today
        label_today = qtw.QLabel(f"Today is {current_date}")
        label_today.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(label_today, alignment=Qt.AlignTop | Qt.AlignRight)

        # create a QLabel object to display the time
        self.uf_current_time = qtw.QLabel(self)
        self.uf_current_time.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(self.uf_current_time, alignment=Qt.AlignTop | Qt.AlignRight)

        # start the timer to update the label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # update every 1 second

        # Customer form header
        cust_header = qtw.QLabel("Customer Form")
        cust_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_cust_form.py
        cust_entry_button = qtw.QPushButton("Add New Customer", clicked = lambda: goto_page("aharts_cust_form.py"))
        self.layout().addWidget(cust_entry_button)

        # call aharts_edit_customer.py
        cust_edit_button = qtw.QPushButton("Edit Customer Information", clicked = lambda: goto_page("aharts_edit_customer.py"))
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
        cust_db_button = qtw.QPushButton("View Customer Database", clicked = lambda: goto_page("database_viewer.py"))
        self.layout().addWidget(cust_db_button)

        # refresh page
        reload_button = qtw.QPushButton("RELOAD PAGE", clicked = lambda: goto_page("main.py"))
        reload_button.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(reload_button)

        # This part is very IMPORTANT!!
        self.show()

        # To call ticket form
        def ticket_entry_form():
            print("Wala pa. Wag kang excited")

    # This code updates uf_current_time every seconds
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.uf_current_time.setText(current_time)

app = qtw.QApplication([])
mw = MainWindow()

app.exec_()
