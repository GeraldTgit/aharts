# Anthony's Home Appliance Repair Ticketing System 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os

# Customize scripts
from create_service_ticket import ServiceTicketWindow
from add_new_customer_backend import *
from database_viewer import *
from logs_generator import *
from public_backend import *
from goto_page import *

class AddNew_CustWindow(QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Add New Customer")
        # Userform layout
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(QIcon(tsys_icon()))

        # SETUP EVERYTHING FIRST

        # Define the constant for font and style properties # PLACEHOLDER
        txtbox_default_font = QFont('Arial', 9, italic=True)
        txtbox_default_style = 'color: gray;'

        # Define the constant for font and style properties # WHEN CHANGE
        txtbox_write_font = QFont('Arial', 9, italic=False)
        txtbox_write_style = "color: black"

        # Text box's write mode
        def write_mode(entry_box):
            entry_box.setFont(txtbox_write_font)
            entry_box.setStyleSheet(txtbox_write_style)

        # Userform Entry box for customer identification type
        with open(os.getcwd()+'/param/id_type.txt', 'r') as file:
            items = file.readlines()

        # Userform header
        uf_header = QLabel("Anthony's Home Appliance-Repair Ticketing System")
        uf_header.setFont(QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform header Customer Information
        uf_cust_info = QLabel("Customer Information: ")
        uf_cust_info.setFont(QFont('Arial', 15))
        self.layout().addWidget(uf_cust_info)

        # Userform header Customer ID number
        uf_cust_tnum = QLabel("Tracking Number is auto-generated for new customers")
        uf_cust_tnum.setFont(QFont('Arial', 9, italic=True))
        self.layout().addWidget(uf_cust_tnum)

        # Userform header Customer First Name
        uf_cust_fname = QLabel("First Name: ")
        uf_cust_fname.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_fname)

        # Userform Entry box for customer First Name
        uf_cust_fname_entry = QLineEdit()
        uf_cust_fname_entry.setPlaceholderText("Given name")
        uf_cust_fname_entry.setObjectName("fname_field")
        self.layout().addWidget(uf_cust_fname_entry)

        # Userform header Customer Last Name
        uf_cust_lname = QLabel("Last Name: ")
        uf_cust_lname.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name 
        uf_cust_lname_entry = QLineEdit()
        uf_cust_lname_entry.setPlaceholderText("Surname")
        uf_cust_lname_entry.setObjectName("lname_field")
        self.layout().addWidget(uf_cust_lname_entry)

        # Userform header Customer Contact Number
        uf_cust_cnum = QLabel("Contact Number: ")
        uf_cust_cnum.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_cnum)

        # Userform Entry box for customer Contact Number
        uf_cust_cnum_entry = QLineEdit()
        uf_cust_cnum_entry.setObjectName("cnum_field")
        uf_cust_cnum_entry.setPlaceholderText("(+63)-917-123-1234")
        self.layout().addWidget(uf_cust_cnum_entry)

        # Userform header Customer Email Address
        uf_cust_email = QLabel("Email Address: ")
        uf_cust_email.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_email)

        # Userform Entry box for customer Email Address
        uf_cust_email_entry = QLineEdit()
        uf_cust_email_entry.setObjectName("Email_field")
        uf_cust_email_entry.setPlaceholderText("username@domain.com")
        self.layout().addWidget(uf_cust_email_entry)

        # Userform header Customer Home Address
        uf_cust_hadd = QLabel("Home Address: ")
        uf_cust_hadd.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_hadd)

        # Userform Entry box for customer Home Address
        uf_cust_hadd_entry = QLineEdit()
        uf_cust_hadd_entry.setObjectName("Hadd_field")
        uf_cust_hadd_entry.setPlaceholderText("Home# Street Name, Barangay, City Name Province Zip Code")
        self.layout().addWidget(uf_cust_hadd_entry)

        # Userform header Customer identification type
        uf_cust_pid = QLabel("Presented ID: ")
        uf_cust_pid.setFont(QFont('Arial', 9))
        self.layout().addWidget(uf_cust_pid)

        uf_cust_pid_entry = QComboBox()        
        # add the items to the combobox
        uf_cust_pid_entry.currentTextChanged.connect(lambda: write_mode(uf_cust_pid_entry))
        uf_cust_pid_entry.addItems([item.strip() for item in items])
        uf_cust_pid_entry.setObjectName("pid_field")
        self.layout().addWidget(uf_cust_pid_entry)

        # Setting up default font and style for text boxes
        textbox_widgets = [uf_cust_fname_entry, uf_cust_lname_entry, uf_cust_cnum_entry, uf_cust_email_entry, uf_cust_hadd_entry]
        #for textbox in textbox_widgets:
        uf_cust_pid_entry.setFont(txtbox_default_font)
        uf_cust_pid_entry.setStyleSheet(txtbox_default_style)

        # Userform header Customer actual identification
        uf_cust_aid = QLabel("Identification")
        uf_cust_aid.setFont(QFont('Arial', 9))
        uf_cust_aid.setOpenExternalLinks(True)  # Enable opening links in a web browser
        uf_cust_aid.linkActivated.connect(self.label_clicked)
        self.layout().addWidget(uf_cust_aid)

        # Upload ID button
        uf_cust_uid_button = QPushButton("Upload ID", clicked = lambda: open_file())
        self.layout().addWidget(uf_cust_uid_button)

        # Save button
        uf_cust_save_button = QPushButton("Save", clicked = lambda: save_it())
        self.layout().addWidget(uf_cust_save_button)

        # Clear all fields buttonl
        uf_cust_clear_button = QPushButton("Clear All", clicked = lambda: clear_all())
        self.layout().addWidget(uf_cust_clear_button)

        # Open database button
        cust_db_button = QPushButton("View Customer Database", clicked = lambda: goto_page("database_viewer.py"))
        self.layout().addWidget(cust_db_button)

        # refresh page
        to_main_button = QPushButton("Back to Main", clicked = lambda: goto_page("main.py"))
        self.layout().addWidget(to_main_button)

        # Choose for ID to upload  
        def open_file():
            options = QFileDialog.Options()
            file_filter = "Image files (*.*)"
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileNames(None, "Select an image file", "", file_filter, options=options)

            # Check if file(s) were selected
            if file_name:
                # Assign the link
                uf_cust_aid.setText(f'<a href="{file_name[0]}">{file_name[0]}</a>')
                uf_cust_uid_button.setText("ID Updated")

        # This part is very IMPORTANT!!
        self.show()

        # To confirm if user wants to save update
        def save_it():       
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AHARTS")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(QMessageBox)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                # Save and closes customer_db() in excel application if open
                save_and_close_database(customer_db())

                # Transferring the selected file to /../temp_db/id/  
                destination_path = upload_identification(uf_cust_aid.text())
                
                # List customer information
                customer_info = [cust_info.text() for cust_info in textbox_widgets] + [uf_cust_pid_entry.currentText(),destination_path]
                
                # Save new customer to database
                save_new(customer_info)
                # Reset components values               
                clear_all()    
                open_create_service_ticket_window(self)


        def open_create_service_ticket_window(self):
            # Show the other user form and hide the main form
            # Create an instance of the other user form
            self.create_service_ticket_window = ServiceTicketWindow()
            # Add the other user form to the layout of the main form
            self.layout().addLayout(self.create_service_ticket_window.layout())
            self.create_service_ticket_window.show()
            self.hide()

        # Clear all fields button
        def clear_all():
            for textbox in textbox_widgets:
                textbox.clear()
            uf_cust_pid_entry.setCurrentIndex(-1)
            uf_cust_uid_button.setText("Upload ID")
            uf_cust_aid.setText("Identification")

    def label_clicked(self, url):
    # Handle the label click event
        print(f"Label clicked: {url}")

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = AddNew_CustWindow()
    mw.show()
    sys.exit(app.exec_())'''
