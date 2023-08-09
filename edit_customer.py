# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
from backend.edit_customer_backend import *
from database_viewer import *
from backend.logs_generator import *
from backend.goto_page import return_to_previous_page

class Edit_CustWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS - Edit Customer Information")
        # Userform layout
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

        def look_up_cust():
            write_mode(cust_tnum_input_entry)
            # Get the search query from the entry box parse
            search_query = validate_num_text(cust_tnum_input_entry)

            # Read the Parquet file into a DataFrame
            cust_info = look_up_cust_info(search_query)
            
            if cust_info:
                # Show customer information in the textboxes
                uf_cust_info.setText("Customer Information: ")
                cust_fname_input.setText(cust_info[0])
                cust_lname_input.setText(cust_info[1])
                cust_contact_num_input.setText(cust_info[2])
                cust_email_input.setText(cust_info[3])
                cust_hadd_input.setText(cust_info[4])
                cust_id_type_input_entry.setCurrentText(cust_info[5])
                try:
                    cust_id_lbl.setText(f'<a href="{id_db_dir+cust_info[6]}">{cust_info[6]}</a>')
                except: 
                    pass
            else:
                uf_cust_info.setText("Customer Information: <b>NO RECORD FOUND</b>")
                clear_all()

        # Userform header
        main_header = QLabel(my_main_header)
        main_header.setFont(QFont('Arial', 20))
        self.layout.addWidget(main_header)

        # Userform header Customer Information
        uf_cust_info = QLabel("Customer Information: ")
        uf_cust_info.setFont(QFont('Arial', 15))
        self.layout.addWidget(uf_cust_info)

        # Userform header Customer ID number
        cust_tnum_input = QLabel("Tracking Number: ")
        cust_tnum_input.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_tnum_input)

        # Userform Entry box for customer First Name
        cust_tnum_input_entry = QLineEdit()
        cust_tnum_input_entry.textChanged.connect(look_up_cust)
        cust_tnum_input_entry.setObjectName("tnum_field")
        cust_tnum_input_entry.setPlaceholderText("Input customer tracking number here.. .")
        self.layout.addWidget(cust_tnum_input_entry)

        # Userform header Customer First Name
        uf_cust_fname = QLabel("First Name: ")
        uf_cust_fname.setFont(QFont('Arial', 9))
        self.layout.addWidget(uf_cust_fname)

        # Userform Entry box for customer First Name
        cust_fname_input = QLineEdit()
        cust_fname_input.textChanged.connect(lambda: write_mode(cust_fname_input))
        cust_fname_input.setPlaceholderText("Given name")
        cust_fname_input.setObjectName("fname_field")
        self.layout.addWidget(cust_fname_input)

        # Userform header Customer Last Name
        uf_cust_lname = QLabel("Last Name: ")
        uf_cust_lname.setFont(QFont('Arial', 9))
        self.layout.addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name 
        cust_lname_input = QLineEdit()
        cust_lname_input.textChanged.connect(lambda: write_mode(cust_lname_input))
        cust_lname_input.setPlaceholderText("Surname")
        cust_lname_input.setObjectName("lname_field")
        self.layout.addWidget(cust_lname_input)

        # Userform header Customer Contact Number
        uf_cust_cnum = QLabel("Contact Number: ")
        uf_cust_cnum.setFont(QFont('Arial', 9))
        self.layout.addWidget(uf_cust_cnum)

        # Userform Entry box for customer Contact Number
        cust_contact_num_input = QLineEdit()
        cust_contact_num_input.textChanged.connect(lambda: write_mode(cust_contact_num_input))
        cust_contact_num_input.setObjectName("cnum_field")
        cust_contact_num_input.setPlaceholderText("(+63)-917-123-1234")
        self.layout.addWidget(cust_contact_num_input)

        # Userform header Customer Email Address
        uf_cust_email = QLabel("Email Address: ")
        uf_cust_email.setFont(QFont('Arial', 9))
        self.layout.addWidget(uf_cust_email)

        # Userform Entry box for customer Email Address
        cust_email_input = QLineEdit()
        cust_email_input.textChanged.connect(lambda: write_mode(cust_email_input))
        cust_email_input.setObjectName("Email_field")
        cust_email_input.setPlaceholderText("username@domain.com")
        self.layout.addWidget(cust_email_input)

        # Userform header Customer Home Address
        uf_cust_hadd = QLabel("Home Address: ")
        uf_cust_hadd.setFont(QFont('Arial', 9))
        self.layout.addWidget(uf_cust_hadd)

        # Userform Entry box for customer Home Address
        cust_hadd_input = QLineEdit()
        cust_hadd_input.textChanged.connect(lambda: write_mode(cust_hadd_input))
        cust_hadd_input.setObjectName("Hadd_field")
        cust_hadd_input.setPlaceholderText("Home# Street Name, Barangay, City Name Province Zip Code")
        self.layout.addWidget(cust_hadd_input)

        # Userform header Customer identification type
        cust_id_type_input = QLabel("Presented ID: ")
        cust_id_type_input.setFont(QFont('Arial', 9))
        self.layout.addWidget(cust_id_type_input)

        cust_id_type_input_entry = QComboBox()        
        # add the items to the combobox
        cust_id_type_input_entry.currentTextChanged.connect(lambda: write_mode(cust_id_type_input_entry))
        cust_id_type_input_entry.addItems([item.strip() for item in items])
        cust_id_type_input_entry.setObjectName("pid_field")
        self.layout.addWidget(cust_id_type_input_entry)

        # Setting up default font and style for text boxes
        textbox_widgets = [cust_fname_input, cust_lname_input, cust_contact_num_input, cust_email_input, cust_hadd_input]
        for textbox in textbox_widgets:
            textbox.setFont(txtbox_default_font)
            textbox.setStyleSheet(txtbox_default_style)

        othertxtb_widgets = [cust_tnum_input_entry, cust_id_type_input_entry]
        for other_txtbox in othertxtb_widgets:
            other_txtbox.setFont(txtbox_default_font)
            other_txtbox.setStyleSheet(txtbox_default_style)

        # Userform header Customer actual identification
        cust_id_lbl = QLabel("Identification")
        cust_id_lbl.setFont(QFont('Arial', 9))
        cust_id_lbl.setOpenExternalLinks(True)  # Enable opening links in a web browser
        cust_id_lbl.linkActivated.connect(self.label_clicked)
        self.layout.addWidget(cust_id_lbl)

        #########################################################################
        # BUTTONS
        #########################################################################

        # Upload ID button
        uf_cust_uid_button = QPushButton("Upload ID", clicked = lambda: open_file())
        self.layout.addWidget(uf_cust_uid_button)

        # Draw a horizontal line
        self.layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # create a QHBoxLayout() to hold the buttons
        buttons_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save", clicked = lambda: check_before_saveit())
        buttons_layout.addWidget(save_button)

        # Clear all fields buttonl
        clear_button = QPushButton("Clear All", clicked = lambda: clear_all())
        buttons_layout.addWidget(clear_button)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # create a QHBoxLayout() to hold the buttons
        buttons_layout = QHBoxLayout()

        # Open database button
        cust_db_btn = QPushButton("View Customer Database", clicked = lambda: open_cust_database_viewer(self))
        buttons_layout.addWidget(cust_db_btn)

        # Go back to main page
        goback_btn = QPushButton("Go Back", clicked = lambda: return_to_previous_page(self, main_window))
        buttons_layout.addWidget(goback_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # This part is very IMPORTANT!!
        self.show()

        ########################################################
        # FUNCTIONS
        ########################################################

        # Upload ID        
        def open_file():
            options = QFileDialog.Options()
            file_filter = "Image files (*.*)"
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getOpenFileNames(None, "Select an image file", "", file_filter, options=options)

            # Check if file(s) were selected
            if file_name:
                # Assign the link
                cust_id_lbl.setText(f'<a href="{file_name[0]}">{file_name[0]}</a>')
                uf_cust_uid_button.setText("ID Updated")

    
        def check_before_saveit():
            if cust_tnum_input_entry.text().isdigit() and cust_tnum_input_entry.text() != "" and uf_cust_info.text() != "Customer Information: <b>NO RECORD FOUND</b>":
                save_it()
            else:
                QMessageBox.information(None, "AHARTS", "Please enter a valid customer tracking number.")

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
                # Transferring the selected file to /../temp_db/id/
                update_id_path = "no"   
                if uf_cust_uid_button.text() == "ID Updated":
                    update_id_path = "yes" 

                # Upload ID if updated
                destination_path = upload_identification(cust_id_lbl.text(),update_id_path)
                
                # List customer information
                customer_info = [cust_tnum_input_entry.text()] + [cust_info.text() for cust_info in textbox_widgets] + [cust_id_type_input_entry.currentText(),destination_path]
                save_update(customer_info)    

                # Reset components values
                clear_all()

        # Clear all fields button
        def clear_all():
            for textbox in textbox_widgets:
                textbox.setText("")
                write_mode(textbox)
            cust_id_type_input_entry.setCurrentIndex(-1)
            uf_cust_uid_button.setText("Upload ID")
            cust_id_lbl.setText("Identification")
            cust_id_lbl.setStyleSheet(txtbox_write_style)       

    def label_clicked(self, url):
    # Handle the label click event
        print(f"Label clicked: {url}")

    def closeEvent(self, event):
        return_to_previous_page(self, self.main_window)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = Edit_CustWindow()
    mw.show()
    sys.exit(app.exec_())
'''    #'''
