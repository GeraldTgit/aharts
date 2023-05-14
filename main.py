# Anthony's Home Appliance Repair Ticketing System
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import datetime
from PyQt5.QtCore import QTimer
import subprocess

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
        self.setWindowTitle("AHARTS")
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
        cust_entry_button = qtw.QPushButton("Add/Update Customer Information", clicked = lambda: cust_entry_form())
        self.layout().addWidget(cust_entry_button)

        # Ticket form header
        cust_header = qtw.QLabel("Ticket Form")
        cust_header.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(cust_header)

        # call aharts_ticket_entry.py
        ticket_entry_button = qtw.QPushButton("Add/Update Service Ticket", clicked = lambda: ticket_entry_form())
        self.layout().addWidget(ticket_entry_button)

        # call aharts_cust_entry.py
        reload_button = qtw.QPushButton("RELOAD PAGE", clicked = lambda: reload())
        self.layout().addWidget(reload_button)

        # This part is very IMPORTANT!!
        self.show()

        # To call customer form
        def cust_entry_form():
            subprocess.run(["python", "aharts_cust_form.py"])

        # To call ticket form
        def ticket_entry_form():
            print("Wala pa. Wag kang excited")

        # To reload the page
        def reload():
            print("Sorry.. still not working")

    # This code updates uf_current_time every seconds
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.uf_current_time.setText("                                                                                                                                                                                                                              " + current_time)

app = qtw.QApplication([])
mw = MainWindow()

app.exec_()
