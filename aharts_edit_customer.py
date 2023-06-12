# Anthony's Home Appliance Repair Ticketing System
from PyQt5.QtWidgets import QMessageBox
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import win32com.client as win32
import subprocess
import tempfile
import datetime
import shutil
import os
import sys
import csv

# Customize scripts
from edit_customer_backend import *
from database_viewer import *
from logs_generator import *
from goto_page import *

class CustWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Edit Customer Information")
        # Userform layout
        self.setLayout(qtw.QVBoxLayout())

        # SETUP EVERYTHING FIRST
        # A destination folder where customer information will be saved
        pwd_ = os.getcwd().replace('\\','/')  
        temp_db = pwd_+"/temp_db/"

        # last/hisghest customer id
        customer_db = temp_db+"customer.csv"

        # Define the constant for font and style properties # PLACEHOLDER
        txtbox_default_font = qtg.QFont('Arial', 9, italic=True)
        txtbox_default_style = 'color: gray;'

        # Define the constant for font and style properties # WHEN CHANGE
        txtbox_write_font = qtg.QFont('Arial', 9, italic=False)
        txtbox_write_style = "color: black"

        # Text box's write mode
        def write_mode(entry_box):
            entry_box.setFont(txtbox_write_font)
            entry_box.setStyleSheet(txtbox_write_style)

        # Userform Entry box for customer identification type
        with open(os.getcwd()+'/param/id_type.txt', 'r') as file:
            items = file.readlines()

        # Look for customer information based on tracking number
        def look_up_cust():     
            write_mode(uf_cust_tnum_entry)      
            # Get the search query from the entry box
            search_query = uf_cust_tnum_entry.text()
            # Open the CSV file and search for the customer information
            with open(customer_db, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if search_query in row:
                        uf_cust_tnum.setText("Tracking Number:")
                        # Customer information found, show in the textboxes
                        uf_cust_fname_entry.setText(row[1])
                        uf_cust_lname_entry.setText(row[2])
                        uf_cust_cnum_entry.setText(row[3])
                        uf_cust_email_entry.setText(row[4])
                        uf_cust_hadd_entry.setText(row[5])
                        uf_cust_pid_entry.setCurrentText(row[6])
                        uf_cust_aid.setText(f'<a href="{row[7]}">{row[7]}</a>')
                        break
                    
                    uf_cust_tnum.setText("Tracking Number: NO RECORD FOUND") 
                    clear_all()

        # Userform header
        uf_header = qtw.QLabel("Anthony's Home Appliance-Repair Ticketing System")
        uf_header.setFont(qtg.QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform header Customer Information
        uf_cust_info = qtw.QLabel("Customer Information: ")
        uf_cust_info.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(uf_cust_info)

        # Userform header Customer ID number
        uf_cust_tnum = qtw.QLabel("Tracking Number: ")
        uf_cust_tnum.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_tnum)

        # Userform Entry box for customer First Name
        uf_cust_tnum_entry = qtw.QLineEdit()
        uf_cust_tnum_entry.textChanged.connect(look_up_cust)
        uf_cust_tnum_entry.setObjectName("tnum_field")
        uf_cust_tnum_entry.setPlaceholderText("Input customer tracking number here.. .")
        self.layout().addWidget(uf_cust_tnum_entry)

        # Userform header Customer First Name
        uf_cust_fname = qtw.QLabel("First Name: ")
        uf_cust_fname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_fname)

        # Userform Entry box for customer First Name
        uf_cust_fname_entry = qtw.QLineEdit()
        uf_cust_fname_entry.textChanged.connect(lambda: write_mode(uf_cust_fname_entry))
        uf_cust_fname_entry.setPlaceholderText("Given name")
        uf_cust_fname_entry.setObjectName("fname_field")
        self.layout().addWidget(uf_cust_fname_entry)

        # Userform header Customer Last Name
        uf_cust_lname = qtw.QLabel("Last Name: ")
        uf_cust_lname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name 
        uf_cust_lname_entry = qtw.QLineEdit()
        uf_cust_lname_entry.textChanged.connect(lambda: write_mode(uf_cust_lname_entry))
        uf_cust_lname_entry.setPlaceholderText("Surname")
        uf_cust_lname_entry.setObjectName("lname_field")
        self.layout().addWidget(uf_cust_lname_entry)

        # Userform header Customer Contact Number
        uf_cust_cnum = qtw.QLabel("Contact Number: ")
        uf_cust_cnum.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_cnum)

        # Userform Entry box for customer Contact Number
        uf_cust_cnum_entry = qtw.QLineEdit()
        uf_cust_cnum_entry.textChanged.connect(lambda: write_mode(uf_cust_cnum_entry))
        uf_cust_cnum_entry.setObjectName("cnum_field")
        uf_cust_cnum_entry.setPlaceholderText("(+63)-917-123-1234")
        self.layout().addWidget(uf_cust_cnum_entry)

        # Userform header Customer Email Address
        uf_cust_email = qtw.QLabel("Email Address: ")
        uf_cust_email.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_email)

        # Userform Entry box for customer Email Address
        uf_cust_email_entry = qtw.QLineEdit()
        uf_cust_email_entry.textChanged.connect(lambda: write_mode(uf_cust_email_entry))
        uf_cust_email_entry.setObjectName("Email_field")
        uf_cust_email_entry.setPlaceholderText("username@domain.com")
        self.layout().addWidget(uf_cust_email_entry)

        # Userform header Customer Home Address
        uf_cust_hadd = qtw.QLabel("Home Address: ")
        uf_cust_hadd.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_hadd)

        # Userform Entry box for customer Home Address
        uf_cust_hadd_entry = qtw.QLineEdit()
        uf_cust_hadd_entry.textChanged.connect(lambda: write_mode(uf_cust_hadd_entry))
        uf_cust_hadd_entry.setObjectName("Hadd_field")
        uf_cust_hadd_entry.setPlaceholderText("Home# Street Name, Barangay, City Name Province Zip Code")
        self.layout().addWidget(uf_cust_hadd_entry)

        # Userform header Customer identification type
        uf_cust_pid = qtw.QLabel("Presented ID: ")
        uf_cust_pid.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_pid)

        uf_cust_pid_entry = qtw.QComboBox()        
        # add the items to the combobox
        uf_cust_pid_entry.currentTextChanged.connect(lambda: write_mode(uf_cust_pid_entry))
        uf_cust_pid_entry.addItems([item.strip() for item in items])
        uf_cust_pid_entry.setObjectName("pid_field")
        self.layout().addWidget(uf_cust_pid_entry)

        # Setting up default font and style for text boxes
        textbox_widgets = [uf_cust_fname_entry, uf_cust_lname_entry, uf_cust_cnum_entry, uf_cust_email_entry, uf_cust_hadd_entry]
        for textbox in textbox_widgets:
            textbox.setFont(txtbox_default_font)
            textbox.setStyleSheet(txtbox_default_style)

        othertxtb_widgets = [uf_cust_tnum_entry, uf_cust_pid_entry]
        for other_txtbox in othertxtb_widgets:
            other_txtbox.setFont(txtbox_default_font)
            other_txtbox.setStyleSheet(txtbox_default_style)

        # Userform header Customer actual identification
        uf_cust_aid = qtw.QLabel("Identification")
        uf_cust_aid.setFont(qtg.QFont('Arial', 9))
        uf_cust_aid.setOpenExternalLinks(True)  # Enable opening links in a web browser
        uf_cust_aid.linkActivated.connect(self.label_clicked)
        self.layout().addWidget(uf_cust_aid)

        # Upload ID button
        uf_cust_uid_button = qtw.QPushButton("Upload ID", clicked = lambda: open_file())
        self.layout().addWidget(uf_cust_uid_button)

        # Save button
        uf_cust_save_button = qtw.QPushButton("Save", clicked = lambda: check_before_saveit())
        self.layout().addWidget(uf_cust_save_button)

        # Clear all fields button
        uf_cust_clear_button = qtw.QPushButton("Clear All", clicked = lambda: clear_all())
        uf_cust_clear_button.clicked.connect(lambda: uf_cust_tnum_entry.setText(""))
        self.layout().addWidget(uf_cust_clear_button)

        # Open database button
        cust_db_button = qtw.QPushButton("View Customer Database", clicked = lambda: goto_page("database_viewer.py"))
        self.layout().addWidget(cust_db_button)

        # refresh page
        to_main_button = qtw.QPushButton("Back to Main", clicked = lambda: goto_page("main.py"))
        self.layout().addWidget(to_main_button)

        # Upload ID        
        def open_file():
            options = qtw.QFileDialog.Options()
            file_filter = "Image files (*.*)"
            options |= qtw.QFileDialog.DontUseNativeDialog
            file_name, _ = qtw.QFileDialog.getOpenFileNames(None, "Select an image file", "", file_filter, options=options)

            # Check if file(s) were selected
            if file_name:
                # Assign the link
                uf_cust_aid.setText(f'<a href="{file_name[0]}">{file_name[0]}</a>')
                uf_cust_uid_button.setText("ID Updated")

        # This part is very IMPORTANT!!
        self.show()

        def check_before_saveit():
            if uf_cust_tnum_entry.text().isdigit() and uf_cust_tnum_entry.text() != "":
                save_it()
            else:
                qtw.QMessageBox.information(None, "AHARTS", "Customer Tracking Number is required!")

        # To confirm if user wants to save update
        def save_it():
            # Close the customer_db Excel application so it can save changes
            save_and_close_database(customer_db)

            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AHARTS")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(qtw.QMessageBox)

            returnValue = msgBox.exec()

            if returnValue == qtw.QMessageBox.Ok:
                # Transferring the selected file to /../temp_db/id/
                update = "no"   
                if uf_cust_uid_button.text() == "ID Updated":
                    update = "yes" 

                # Upload ID if updated
                destination_path = upload_identification(uf_cust_aid.text(),update)
                
                customer_info = [uf_cust_tnum_entry.text()] + [cust_info.text() for cust_info in textbox_widgets] + [uf_cust_pid_entry.currentText(),destination_path]
                save_update(customer_info)    

                # Reset components values
                clear_all()

        # Clear all fields button
        def clear_all():
            for textbox in textbox_widgets:
                textbox.setText("")
                write_mode(textbox)
            uf_cust_pid_entry.setCurrentIndex(-1)
            uf_cust_uid_button.setText("Upload ID")
            uf_cust_aid.setText("Identification")
            uf_cust_aid.setStyleSheet(txtbox_write_style)       

    def label_clicked(self, url):
    # Handle the label click event
        print(f"Label clicked: {url}")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = CustWindow()
    mw.show()
    sys.exit(app.exec_())
