# Anthony's Home Appliance Repair Ticketing System
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import subprocess
import shutil
import os
import sys
import csv
import tempfile

class CustWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS")
        # Userform layout
        self.setLayout(qtw.QVBoxLayout())
        #self.initUI()

        # A destination folder where you want to move the selected file
        pwd_ = os.getcwd()
        temp_db = pwd_+"/temp_db/"

        # last/hisghest customer id
        customer_db = temp_db+"customer.csv"

        # Getting things ready
        # Check if the customer.csv file exists in the customer_db directory
        if not os.path.isfile(customer_db):
            # Create a new customer.csv file with headers
            headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Home Address', 'ID Type', 'ID Path']
            with open(customer_db, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

        # Look for customer information based on tracking number
        def look_up_cust():
            #uf_cust_fname_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            #uf_cust_fname_entry.setStyleSheet("color: black")
            # Get the search query from the entry box
            search_query = uf_cust_tnum_entry.text()
            # Open the CSV file and search for the customer information
            with open(customer_db, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if search_query in row:
                        # Customer information found, do something with it
                        uf_cust_fname_entry.setText(row[1])
                        uf_cust_lname_entry.setText(row[2])
                        uf_cust_cnum_entry.setText(row[3])
                        uf_cust_Email_entry.setText(row[4])
                        uf_cust_Hadd_entry.setText(row[5])
                        uf_cust_pid_entry.setCurrentText(row[6])
                        uf_cust_aid.setText(row[7])
                        break

        # Reset input boxes design
        def reset_design_fname():
            uf_cust_fname_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_fname_entry.setStyleSheet("color: black")

        def reset_design_lname():
            uf_cust_lname_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_lname_entry.setStyleSheet("color: black")

        def reset_design_cnum():
            uf_cust_cnum_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_cnum_entry.setStyleSheet("color: black")

        def reset_design_Email():
            uf_cust_Email_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_Email_entry.setStyleSheet("color: black")

        def reset_design_Hadd():
            uf_cust_Hadd_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_Hadd_entry.setStyleSheet("color: black")

        def reset_design_pid():
            uf_cust_pid_entry.setFont(qtg.QFont('Arial', 9, italic=False))
            uf_cust_pid_entry.setStyleSheet("color: black")

        # Userform header
        uf_header = qtw.QLabel("Anthony's Home Appliance Repair Ticketing System")
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
        uf_cust_tnum_entry.setObjectName("fname_field")
        self.layout().addWidget(uf_cust_tnum_entry)

        # Userform header Customer First Name
        uf_cust_fname = qtw.QLabel("First Name: ")
        uf_cust_fname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_fname)

        # Userform Entry box for customer First Name
        uf_cust_fname_entry = qtw.QLineEdit()
        uf_cust_fname_entry.textChanged.connect(reset_design_fname)
        uf_cust_fname_entry.setText("Given name")
        uf_cust_fname_entry.setObjectName("fname_field")
        uf_cust_fname_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_fname_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_fname_entry)

        # Userform header Customer Last Name
        uf_cust_lname = qtw.QLabel("Last Name: ")
        uf_cust_lname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name 
        uf_cust_lname_entry = qtw.QLineEdit()
        uf_cust_lname_entry.textChanged.connect(reset_design_lname)
        uf_cust_lname_entry.setText("Surname")
        uf_cust_lname_entry.setObjectName("lname_field")
        uf_cust_lname_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_lname_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_lname_entry)

        # Userform header Customer Contact Number
        uf_cust_cnum = qtw.QLabel("Contact Number: ")
        uf_cust_cnum.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_cnum)

        # Userform Entry box for customer Contact Number
        uf_cust_cnum_entry = qtw.QLineEdit()
        uf_cust_cnum_entry.textChanged.connect(reset_design_cnum)
        uf_cust_cnum_entry.setObjectName("cnum_field")
        uf_cust_cnum_entry.setText("+63-917-123-1234")
        uf_cust_cnum_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_cnum_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_cnum_entry)

        # Userform header Customer Email Address
        uf_cust_Email = qtw.QLabel("Email Address: ")
        uf_cust_Email.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_Email)

        # Userform Entry box for customer Email Address
        uf_cust_Email_entry = qtw.QLineEdit()
        uf_cust_Email_entry.textChanged.connect(reset_design_Email)
        uf_cust_Email_entry.setObjectName("Email_field")
        uf_cust_Email_entry.setText("username@domain.com")
        uf_cust_Email_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_Email_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_Email_entry)

        # Userform header Customer Home Address
        uf_cust_Hadd = qtw.QLabel("Home Address: ")
        uf_cust_Hadd.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_Hadd)

        # Userform Entry box for customer Home Address
        uf_cust_Hadd_entry = qtw.QLineEdit()
        uf_cust_Hadd_entry.textChanged.connect(reset_design_Hadd)
        uf_cust_Hadd_entry.setObjectName("Hadd_field")
        uf_cust_Hadd_entry.setText("Home# Street Name, Barangay, City Name Province Zip Code")
        uf_cust_Hadd_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_Hadd_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_Hadd_entry)

        # Userform header Customer identification type
        uf_cust_pid = qtw.QLabel("Presented ID: ")
        uf_cust_pid.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_pid)

        # Userform Entry box for customer identification type
        with open(os.getcwd()+'/param/id_type.txt', 'r') as file:
            items = file.readlines()

        uf_cust_pid_entry = qtw.QComboBox()        
        # add the items to the combobox
        uf_cust_pid_entry.currentTextChanged.connect(reset_design_pid)
        uf_cust_pid_entry.addItems([item.strip() for item in items])
        uf_cust_pid_entry.setObjectName("pid_field")
        uf_cust_pid_entry.setFont(qtg.QFont('Arial', 9, italic=True))
        uf_cust_pid_entry.setStyleSheet('color: gray;')
        self.layout().addWidget(uf_cust_pid_entry)

        # Userform header Customer actual identification
        uf_cust_aid = qtw.QLabel("Identification")
        uf_cust_aid.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_aid)

        # Upload ID button
        uf_cust_uid_button = qtw.QPushButton("Upload ID", clicked = lambda: open_file())
        self.layout().addWidget(uf_cust_uid_button)

        # Save button
        uf_cust_save_button = qtw.QPushButton("Save", clicked = lambda: save_it())
        self.layout().addWidget(uf_cust_save_button)

        # Clear all fields button
        uf_cust_clear_button = qtw.QPushButton("Clear All", clicked = lambda: clear_all())
        self.layout().addWidget(uf_cust_clear_button)

        # refresh page
        reload_button = qtw.QPushButton("Back to Main", clicked = lambda: reload())
        self.layout().addWidget(reload_button)

        # Upload ID
        def open_file():
            #app = qtw.QApplication(sys.argv)
            options = qtw.QFileDialog.Options()
            file_filter = "Image files (*.png *.jpeg *.jpg *.pdf)"
            options |= qtw.QFileDialog.DontUseNativeDialog
            file_name, _ = qtw.QFileDialog.getOpenFileNames(None, "Select an image file", "", file_filter, options=options)

            # Check if file(s) were selected
            if file_name:
                uf_cust_aid.setText(f"ID path: {file_name[0]}")
                uf_cust_aid.setStyleSheet("color: blue")

        # This part is very IMPORTANT!!
        self.show()

        def save_it():
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AARTS")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(qtw.QMessageBox)

            returnValue = msgBox.exec()
            if returnValue == qtw.QMessageBox.Ok:
                # Transferring the selected file to /../temp_db/id/
                if uf_cust_aid.text() != "Identification":
                    shutil.copy(uf_cust_aid.text()[9:], temp_db+"id/")

                saving_it()    

        def saving_it():
            # Get the input values from the user form
            first_name = uf_cust_fname_entry.text()
            last_name = uf_cust_lname_entry.text()
            contact_number = uf_cust_cnum_entry.text()
            email = uf_cust_Email_entry.text()
            home_address = uf_cust_Hadd_entry.text()
            id_type = uf_cust_pid_entry.currentText()
            id_path = uf_cust_aid.text()

            with open(customer_db, 'r') as file:
                reader = csv.reader(file)
                # skip header row if it exists
                if csv.Sniffer().has_header(file.read(1024)):
                    file.seek(0)
                    next(reader)

                try:
                    # Get the max value from the first column or assign 0 if the reader is empty
                    highest_cust_id = max(int(row[0]) for row in reader)
                except ValueError:
                    highest_cust_id = 0

            # Assign a value of 1 if no existing entries
            new_entry_cust_id = highest_cust_id + 1
            
            # Rest of the code to update or append rows
            with open(customer_db, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)

                if len(rows) > 0:
                    for row in rows:
                        if row[0] == uf_cust_tnum_entry.text():
                            # Customer ID already exists, update the row
                            row[1] = first_name
                            row[2] = last_name
                            row[3] = contact_number
                            row[4] = email
                            row[5] = home_address
                            row[6] = id_type
                            row[7] = id_path
                            break
                    else:
                        # Customer ID doesn't exist, append a new row
                        rows.append([new_entry_cust_id, first_name, last_name, contact_number, email, home_address, id_type, id_path])
                else:
                    # Customer.csv is empty, add the headers and append a new row
                    headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Home Address', 'ID Type', 'ID Path']
                    rows.append(headers)
                    rows.append([new_entry_cust_id, first_name, last_name, contact_number, email, home_address, id_type, id_path])

            # Write the modified data back to the file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                with open(temp_file.name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)  # Write the rows

            # Replace the original file with the updated file
            shutil.move(temp_file.name, customer_db) 

            clear_all()

        # Clear all fields button
        def clear_all():
            uf_cust_tnum_entry.setText("")
            uf_cust_fname_entry.setText("")
            uf_cust_lname_entry.setText("")
            uf_cust_cnum_entry.setText("")
            uf_cust_Email_entry.setText("")
            uf_cust_Hadd_entry.setText("")
            uf_cust_pid_entry.setCurrentIndex(-1)
            reset_design_fname()
            reset_design_lname()
            reset_design_cnum()
            reset_design_Email()
            reset_design_Hadd()
            reset_design_pid()
            uf_cust_aid.setText("Identification")
            uf_cust_aid.setStyleSheet("color: black")

        # To reload the page
        def reload():
            # Path to the Python script you want to rerun
            script_path = pwd_+"/reload.py"

            # Define the command to run the new script
            new_script_command = ["python", script_path]

            # Start the new script
            subprocess.Popen(new_script_command)

            # Exit the current script
            sys.exit()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = CustWindow()
    mw.show()
    sys.exit(app.exec_())
