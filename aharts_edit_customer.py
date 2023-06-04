# Anthony's Home Appliance Repair Ticketing System
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import win32com.client as win32
from database_viewer import *
import subprocess
import tempfile
import datetime
import shutil
import os
import sys
import csv

class CustWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Edit Customer Information Page")
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

        # Check if the customer.csv file exists in the customer_db directory
        if not os.path.isfile(customer_db):
            # Create a new customer.csv file with headers
            headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Home Address', 'ID Type', 'ID Path']
            with open(customer_db, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)

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
        uf_cust_fname_entry.textChanged.connect(lambda: write_mode(uf_cust_fname_entry))
        uf_cust_fname_entry.setText("Given name")
        uf_cust_fname_entry.setObjectName("fname_field")
        self.layout().addWidget(uf_cust_fname_entry)

        # Userform header Customer Last Name
        uf_cust_lname = qtw.QLabel("Last Name: ")
        uf_cust_lname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name 
        uf_cust_lname_entry = qtw.QLineEdit()
        uf_cust_lname_entry.textChanged.connect(lambda: write_mode(uf_cust_lname_entry))
        uf_cust_lname_entry.setText("Surname")
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
        uf_cust_cnum_entry.setText("(+63)-917-123-1234")
        self.layout().addWidget(uf_cust_cnum_entry)

        # Userform header Customer Email Address
        uf_cust_email = qtw.QLabel("Email Address: ")
        uf_cust_email.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_email)

        # Userform Entry box for customer Email Address
        uf_cust_email_entry = qtw.QLineEdit()
        uf_cust_email_entry.textChanged.connect(lambda: write_mode(uf_cust_email_entry))
        uf_cust_email_entry.setObjectName("Email_field")
        uf_cust_email_entry.setText("username@domain.com")
        self.layout().addWidget(uf_cust_email_entry)

        # Userform header Customer Home Address
        uf_cust_hadd = qtw.QLabel("Home Address: ")
        uf_cust_hadd.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_hadd)

        # Userform Entry box for customer Home Address
        uf_cust_hadd_entry = qtw.QLineEdit()
        uf_cust_hadd_entry.textChanged.connect(lambda: write_mode(uf_cust_hadd_entry))
        uf_cust_hadd_entry.setObjectName("Hadd_field")
        uf_cust_hadd_entry.setText("Home# Street Name, Barangay, City Name Province Zip Code")
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
        cust_db_button = qtw.QPushButton("View Customer Database", clicked = lambda: open_database_viewer())
        self.layout().addWidget(cust_db_button)

        # refresh page
        reload_button = qtw.QPushButton("Back to Main", clicked = lambda: to_main())
        self.layout().addWidget(reload_button)

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
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            workbook = excel.Workbooks.Open(customer_db)
            # Save changes
            workbook.Save()
            subprocess.call(['taskkill', '/f', '/im', 'EXCEL.EXE'], shell=True)

            # Slicing identification label to get the absolute path only
            id_path = uf_cust_aid.text()
            # Find the index of '<' and '>'
            start_index = id_path.find('=')
            end_index = id_path.find('>')
            # Extract the substring between '=' and '>'
            id_path = id_path[start_index + 1 : end_index] 

            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AHARTS")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(qtw.QMessageBox)

            returnValue = msgBox.exec()

            # assigning default value if no id provided
            destination_path = "No Idenfication provided." 
            if returnValue == qtw.QMessageBox.Ok:
                # Transferring the selected file to /../temp_db/id/
                id_path=id_path.replace('"','')          
                if uf_cust_aid.text() != "Identification":
                    destination_folder = temp_db+"id/"
                    
                    # Get the filename and extension from the source path
                    file_name = os.path.basename(id_path)
                    file_name, file_extension = os.path.splitext(file_name)

                    # Generate the new filename with the current date and time
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    new_file_name = f"{file_name}_{current_date}{file_extension}"

                    # Create the destination path by combining the destination folder and the new filename
                    destination_path = os.path.join(destination_folder, new_file_name)

                    # Copy the file to the destination folder
                    destination_path=destination_path.replace(' ','_')                   
                    try:
                        shutil.copy2(id_path, destination_path)
                    except:
                        pass

                print(destination_path)
                saving_it(destination_path)     
                # if yes proceed saving
                #if uf_cust_uid_button.text == "ID Updated":     
                #    saving_it(destination_path.replace(' ','_'))
                #else:    
                #    saving_it(id_path.replace(' ','_'))    
                # if no do nothing

        # Saving data in the csv file with new name for identification
        def saving_it(new_idpath):
            # Get the input values from the user form
            first_name = uf_cust_fname_entry.text()
            last_name = uf_cust_lname_entry.text()
            contact_number = uf_cust_cnum_entry.text()
            email = uf_cust_email_entry.text()
            home_address = uf_cust_hadd_entry.text()
            id_type = uf_cust_pid_entry.currentText()
            
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
                            row[7] = new_idpath
                            break

            # Write the modified data back to the file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                with open(temp_file.name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)  # Write the rows

            # Replace the original file with the updated file
            shutil.move(temp_file.name, customer_db) 
            # Reset components values
            clear_all()
            uf_cust_tnum_entry.setText("")

        # Clear all fields button
        def clear_all():
            for textbox in textbox_widgets:
                textbox.setText("")
                write_mode(textbox)
            uf_cust_pid_entry.setCurrentIndex(-1)
            uf_cust_uid_button.setText("Upload ID")
            uf_cust_aid.setText("Identification")
            uf_cust_aid.setStyleSheet(txtbox_write_style)       

        # To reload the page
        def to_main():
            # Path to the Python script you want to rerun
            script_path = pwd_+"/reload.py"

            # Define the command to run the new script
            new_script_command = ["python", script_path]

            # Start the new script
            subprocess.Popen(new_script_command)

            # Exit the current script
            sys.exit()

        # To open the customer database view form
        def open_database_viewer():
            # Path to the Python script you want to rerun
            script_path = pwd_+"/database_viewer.py"

            # Define the command to run the new script
            new_script_command = ["python", script_path]

            # Start the new script
            subprocess.Popen(new_script_command)

    def label_clicked(self, url):
    # Handle the label click event
        print(f"Label clicked: {url}")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = CustWindow()
    mw.show()
    sys.exit(app.exec_())
