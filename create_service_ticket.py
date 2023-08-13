# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Sub-pages
from billing import BillingWindow

# Customize scripts
from database_viewer import *
from backend.logs_generator import *
from backend.goto_page import return_to_previous_page
from backend.service_ticket_backend import *

class ServiceTicketWindow(QWidget):
    def __init__(self, main_window,recent_txn_id):
        super().__init__()
        self.setWindowTitle("AHARTS - Create Service Ticket")
        self.layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(tsystem_icon))

        # Store a reference to the main form
        self.main_window = main_window
        self.recent_txn_id = str(recent_txn_id)
             
        # Header
        main_header = QLabel(my_main_header)
        main_header.setFont(QFont('Arial', 20))
        self.layout.addWidget(main_header)

        # Customer Information Section
        cust_info_header = QLabel("Customer Information:")
        cust_info_header.setFont(QFont('Arial', 15))
        self.layout.addWidget(cust_info_header)

        form_layout = QFormLayout()

        # Tracking Number
        cust_tnum = QLabel("Tracking Number:")
        cust_tnum.setFont(QFont('Arial', 9))
        cust_tnum_input = QLineEdit()
        cust_tnum_input.setPlaceholderText("Input customer tracking number here...")
        cust_tnum_input.textChanged.connect(lambda: look_up_cust())
        form_layout.addRow(cust_tnum, cust_tnum_input)

        self.layout.addLayout(form_layout)

    
        # What's customer full name label
        cust_fullname_lbl = QLabel("What's the customer tracking number?")
        cust_fullname_lbl.setFont(QFont('Arial', 12))
        self.layout.addWidget(cust_fullname_lbl)

        # Appliance Information Section
        service_ticket_header = QLabel("Appliance Information:")
        service_ticket_header.setFont(QFont('Arial', 15))
        self.layout.addWidget(service_ticket_header)

        # Drop down options for types of appliances
        appliance_combo_box = QComboBox()
        appliance_combo_box.addItems([appliance.strip() for appliance in appliances()])
        appliance_combo_box.setEditable(True)

        # Textbox placeholder
        brand_input = QLineEdit()
        brand_input.setPlaceholderText("Samsung, Panasonic, LG, etc.")

        model_input = QLineEdit()
        model_input.setPlaceholderText("T-1000")

        issue_input = QLineEdit()
        issue_input.setPlaceholderText("Not responding")

        status_combo_box = QComboBox()
        status_combo_box.addItems([status.strip() for status in service_status()])
        
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Type of Appliance:"), appliance_combo_box)
        form_layout.addRow(QLabel("Brand:"), brand_input)
        form_layout.addRow(QLabel("Model:"), model_input)
        form_layout.addRow(QLabel("Issue:"), issue_input)
        form_layout.addRow(QLabel("Service Status:"), status_combo_box)

        self.layout.addLayout(form_layout)

        # Form Widgets ################################################################################

        textbox_widgets = [cust_tnum_input, brand_input, model_input, issue_input]

        #########################################################################
        # BUTTONS
        #########################################################################

        # Draw a horizontal line
        self.layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save", clicked = lambda: create_ticket())
        buttons_layout.addWidget(save_button)

        # Clear all fields buttonl
        clear_button = QPushButton("Clear All", clicked = lambda: clear_textbox())
        buttons_layout.addWidget(clear_button)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Open database button
        cust_db_btn = QPushButton("View Customer Database", clicked = lambda: open_cust_database_viewer(self))
        buttons_layout.addWidget(cust_db_btn)

        # Go back to main page
        goback_btn = QPushButton("Go Back", clicked = lambda: return_to_previous_page(self, main_window))
        buttons_layout.addWidget(goback_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        self.show()

        ########################################################
        # FUNCTIONS
        ########################################################

        # Look for customer information (name) based on tracking number
        def look_up_cust():
            customer_name = look_up_cust_name(validate_num_text(cust_tnum_input))
            cust_fullname_lbl.setText(f"Customer Name: <b>{customer_name}</b>")  

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
                serv_info.insert(1,appliance_combo_box.currentText())
                serv_info.append(status_combo_box.currentText())
                recent_txn_id = save_new_ticket(serv_info)
                self.open_troubleshootingwindow(recent_txn_id)

        def clear_textbox():
            for textbox in textbox_widgets:
                textbox.clear()

            cust_fullname_lbl.setText("What's the customer tracking number?")


        # Transfer/set latest customer id
        cust_tnum_input.setText(self.recent_txn_id)

    #######################################d#################
    # MORE FUNCTIONS
    ########################################################
    

    def open_troubleshootingwindow(self,recent_txn_id):
        self.hide()
        self.troubleshootingwindow = BillingWindow(self,recent_txn_id)
        self.troubleshootingwindow.show()

    def closeEvent(self, event):
        return_to_previous_page(self, self.main_window)

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = ServiceTicketWindow()
    sys.exit(app.exec_())  
''' #'''
