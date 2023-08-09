# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Sub-pages
from create_service_ticket import ServiceTicketWindow
from backend.goto_page import return_to_previous_page

# Customize scripts
from backend.add_new_customer_backend import *
from database_viewer import *
from backend.logs_generator import *

class AddNewCustWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("AHARTS - Add New Customer")
        self.layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(tsystem_icon))

        # Store a reference to the main form
        self.main_window = main_window

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
        with open(id_type_list_dir, 'r') as file:
            items = file.readlines()

        # Userform header
        main_header = QLabel(my_main_header)
        main_header.setFont(QFont('Arial', 20))
        self.layout.addWidget(main_header)

        # Userform header Customer Information
        cust_info_header = QLabel("Customer Information:")
        cust_info_header.setFont(QFont('Arial', 15))
        self.layout.addWidget(cust_info_header)

        # Userform header Customer ID number
        cust_tnum_lbl = QLabel("Tracking Number is auto-generated for new customer")
        cust_tnum_lbl.setFont(QFont('Arial', 9, italic=True))
        self.layout.addWidget(cust_tnum_lbl)

        # Userform header Customer First Name
        cust_fname_lbl = QLabel("First Name: ")
        cust_fname_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_fname_lbl)

        # Userform Entry box for customer First Name
        self.cust_fname_input = QLineEdit()
        self.cust_fname_input.setPlaceholderText("Given name")
        self.cust_fname_input.setObjectName("fname_field")
        self.layout.addWidget(self.cust_fname_input)

        # Userform header Customer Last Name
        cust_lname_lbl = QLabel("Last Name: ")
        cust_lname_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_lname_lbl)

        # Userform Entry box for customer Last Name 
        self.cust_lname_input = QLineEdit()
        self.cust_lname_input.setPlaceholderText("Surname")
        self.cust_lname_input.setObjectName("lname_field")
        self.layout.addWidget(self.cust_lname_input)

        # Userform header Customer Contact Number
        cust_contact_num_lbl = QLabel("Contact Number: ")
        cust_contact_num_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_contact_num_lbl)

        # Userform Entry box for customer Contact Number
        cust_contact_num_input = QLineEdit()
        cust_contact_num_input.setObjectName("cnum_field")
        cust_contact_num_input.setPlaceholderText("(+63)-917-123-1234")
        self.layout.addWidget(cust_contact_num_input)

        # Userform header Customer Email Address
        cust_email_lbl = QLabel("Email Address: ")
        cust_email_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_email_lbl)

        # Userform Entry box for customer Email Address
        cust_email_input = QLineEdit()
        cust_email_input.setObjectName("Email_field")
        cust_email_input.setPlaceholderText("username@domain.com")
        self.layout.addWidget(cust_email_input)

        # Userform header Customer Home Address
        cust_hadd_lbl = QLabel("Home Address: ")
        cust_hadd_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_hadd_lbl)

        # Userform Entry box for customer Home Address
        cust_hadd_input = QLineEdit()
        cust_hadd_input.setObjectName("Hadd_field")
        cust_hadd_input.setPlaceholderText("Home# Street Name, Barangay, City Name Province Zip Code")
        self.layout.addWidget(cust_hadd_input)

        # Userform header Customer identification type
        cust_id_type_lbl = QLabel("Presented ID: ")
        cust_id_type_lbl.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_id_type_lbl)

        self.cust_id_type_input = QComboBox()        
        # add the items to the combobox
        self.cust_id_type_input.currentTextChanged.connect(lambda: write_mode(self.cust_id_type_input))
        self.cust_id_type_input.addItems([item.strip() for item in items])
        self.cust_id_type_input.setEditable(True)
        self.cust_id_type_input.setObjectName("pid_field")
        self.layout.addWidget(self.cust_id_type_input)

        # Setting up default font and style for text boxes
        self.textbox_widgets = [self.cust_fname_input, self.cust_lname_input, cust_contact_num_input, cust_email_input, cust_hadd_input]
        self.cust_id_type_input.setFont(txtbox_default_font)
        self.cust_id_type_input.setStyleSheet(txtbox_default_style)

        # Userform header Customer actual identification
        self.cust_id_lbl = QLabel("Identification")
        self.cust_id_lbl.setFont(QFont('Arial', 9))
        self.cust_id_lbl.setOpenExternalLinks(True)  # Enable opening links in a web browser
        self.cust_id_lbl.linkActivated.connect(self.label_clicked)
        self.layout.addWidget(self.cust_id_lbl)

        #########################################################################
        # BUTTONS
        #########################################################################

        # Upload ID button
        self.cust_upload_id_btn = QPushButton("Upload ID")
        self.cust_upload_id_btn.clicked.connect(self.open_file)
        self.layout.addWidget(self.cust_upload_id_btn)

        # Draw a horizontal line
        self.layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Save button
        save_btn = QPushButton("Save", clicked = lambda: self.save_it())
        buttons_layout.addWidget(save_btn)

        # Clear all fields buttonl
        clear_btn = QPushButton("Clear All", clicked = lambda: self.clear_all())
        buttons_layout.addWidget(clear_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

       # Open database button
        cust_db_btn = QPushButton("View Customer Database", clicked = lambda: open_cust_database_viewer(self))
        buttons_layout.addWidget(cust_db_btn)

        # Go Back page
        goback_btn = QPushButton("Go Back", clicked = lambda: return_to_previous_page(self, main_window))
        buttons_layout.addWidget(goback_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        ########################################################
        # FUNCTIONS
        ########################################################

        # This part is very IMPORTANT!!
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        file_filter = "Image files (*.*)"
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileNames(None, "Select an image file", "", file_filter, options=options)

        # Check if file(s) were selected
        if file_name:
            # Assign the link
            self.cust_id_lbl.setText(f'<a href="{file_name[0]}">{file_name[0]}</a>')
            self.cust_upload_id_btn.setText("ID Updated")

    def save_it(self):
        if self.cust_fname_input.text() == "" and self.cust_lname_input.text() == "":
            self.cust_fname_input.setText("Guest")

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Are you sure you want to save changes?")
        msgBox.setWindowTitle("AHARTS")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.buttonClicked.connect(QMessageBox)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            # Transferring the selected file to /../temp_db/id/  
            destination_path = upload_identification(self.cust_id_lbl.text())

            # List customer information
            customer_info = [cust_info.text() for cust_info in self.textbox_widgets] + [self.cust_id_type_input.currentText(), destination_path]

            # Save new customer to database
            recent_txn_id = save_new(customer_info)
            # Reset components values               
            self.clear_all()
            # Open Service_ticket window
            self.open_create_service_ticketwindow(recent_txn_id)

    def clear_all(self):
        for textbox in self.textbox_widgets:
            textbox.clear()
        self.cust_id_type_input.setCurrentIndex(-1)
        self.cust_upload_id_btn.setText("Upload ID")
        self.cust_id_lbl.setText("Identification")

    def label_clicked(self, url):
        # Handle the label click event
        print(f"Label clicked: {url}")

    def open_create_service_ticketwindow(self,recent_txn_id):     
        self.hide()
        self.create_service_ticketwindow = ServiceTicketWindow(self,recent_txn_id)
        self.create_service_ticketwindow.show()

    def closeEvent(self, event):
        return_to_previous_page(self, self.main_window)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = AddNew_CustWindow()
    mw.show()
    sys.exit(app.exec_())
'''   #'''
