# Anthony's Home Appliance Repair Ticketing System
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

# Customize scripts
from database_viewer import *
from logs_generator import *
from public_backend import *
from goto_page import *
from service_ticket_backend import *

class ServiceTicketWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AHARTS - Create Service Ticket")
        self.setLayout(QVBoxLayout())

        # Look for customer information based on tracking number
        def look_up_cust():     
            #write_mode(cust_tnum_entry)      
            # Get the search query from the entry box
            search_query = cust_tnum_entry.text()
            # Open the CSV file and search for the customer information
            with open(customer_db(), 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if search_query in row:
                        cust_tnum.setText("Tracking Number:")
                        # Customer information found, show in the textboxes
                        cust_fullname_lbl.setText(f"Customer Name: {row[1]} {row[2]}")
                        #cust_email_entry.setText(row[4])

                        break
                                     
                    cust_fullname_lbl.setText("Customer Information Not Found")


        # Header
        header = QLabel("Anthony's Home Appliance-Repair Ticketing System")
        header.setFont(QFont('Arial', 25))
        self.layout().addWidget(header)

        # Customer Information Section
        cust_info = QLabel("Customer Information:")
        cust_info.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_info)

        form_layout = QFormLayout()

        # Tracking Number
        cust_tnum = QLabel("Tracking Number:")
        cust_tnum.setFont(QFont('Arial', 9))
        cust_tnum_entry = QLineEdit()
        cust_tnum_entry.setPlaceholderText("Input customer tracking number here...")
        cust_tnum_entry.textChanged.connect(look_up_cust)
        form_layout.addRow(cust_tnum, cust_tnum_entry)

        self.layout().addLayout(form_layout)

        # What's customer full name label
        cust_fullname_lbl = QLabel("What's the customer tracking number?")
        cust_fullname_lbl.setFont(QFont('Arial', 12))
        self.layout().addWidget(cust_fullname_lbl)

        # Appliance Information Section
        service_ticket_header = QLabel("Appliance Information:")
        service_ticket_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(service_ticket_header)

        # Drop down options for types of appliances
        appliance_combo_box = QComboBox()
        appliance_combo_box.addItems([appliance.strip() for appliance in appliances()])

        # Textbox placeholder
        brand_txtbox = QLineEdit()
        brand_txtbox.setPlaceholderText("Samsung, Panasonic, LG, etc.")

        model_txtbox = QLineEdit()
        model_txtbox.setPlaceholderText("T-1000")

        issue_txtbox = QLineEdit()
        issue_txtbox.setPlaceholderText("Not responding")

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Type of Appliance:"), appliance_combo_box)
        form_layout.addRow(QLabel("Brand:"), brand_txtbox)
        form_layout.addRow(QLabel("Model:"), model_txtbox)
        form_layout.addRow(QLabel("Issue:"), issue_txtbox)

        self.layout().addLayout(form_layout)

        # Form Widgets ################################################################################

        textbox_widgets = [cust_tnum_entry, brand_txtbox, model_txtbox, issue_txtbox]

        # BUTTONS ##########################################################################################

        # Save button
        cust_save_button = QPushButton("Save", clicked=lambda: create_ticket())
        self.layout().addWidget(cust_save_button)

        # Clear all fields button
        cust_clear_button = QPushButton("Clear All", clicked=lambda: clear_textbox())
        self.layout().addWidget(cust_clear_button)

        # Open database button
        cust_db_button = QPushButton("View Customer Database", clicked=lambda: goto_page("database_viewer.py"))
        self.layout().addWidget(cust_db_button)

        # Back to Main button
        to_main_button = QPushButton("Back to Main", clicked=lambda: goto_page("main.py"))
        self.layout().addWidget(to_main_button)

        self.show()

        def create_ticket():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AHARTS")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(QMessageBox)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                serv_info = [serv_data.text() for serv_data in textbox_widgets]
                serv_info.insert(1, appliance_combo_box.currentText())
                save_new(serv_info)
                goto_page("troubleshooting.py")

        def clear_textbox():
            for textbox in textbox_widgets:
                textbox.clear()

            cust_fullname_lbl.setText("What's the customer tracking number?")

        # Transfer/set latest customer id
        cust_tnum_entry.setText(pyperclip.paste())
        pyperclip.copy('')

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ServiceTicketWindow()
    sys.exit(app.exec_())'''
