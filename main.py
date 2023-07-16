# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
# Sub-pages
from add_new_cust import AddNewCustWindow
from edit_customer import Edit_CustWindow
from create_service_ticket import ServiceTicketWindow
from troubleshooting import TroubleshootingWindow

# Backend scripts
from database_viewer import *
from backend.logs_generator import *
from backend.main_backend import *

# Param checker
setup_log_file()
check_customer_db()
check_serv_ticket_db()
check_troubleshooting_order_db()

current_time = datetime.datetime.now()
current_hour = current_time.hour

# Task bar icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if current_hour < 12:
    greetings = "Good morning!"
elif 12 <= current_hour < 18:
    greetings = "Good afternoon!"
else:
    greetings = "Good evening!"

current_date = current_time.strftime("%A, %B %d, %Y")

# Simply null
null = ""

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AHARTS - Main Menu")
        self.setLayout(QVBoxLayout())
        self.setWindowIcon(QIcon(tsystem_icon))

        # Userform header
        main_header = QLabel(my_main_header)
        main_header.setFont(QFont('Arial', 20))
        self.layout().addWidget(main_header, alignment=Qt.AlignCenter)

        # create a QHBoxLayout to hold the greeting_and_lbl_today_layout
        greeting_and_lbl_today_layout = QHBoxLayout()

        # Userform greeting
        greeting_header = QLabel(f"Hi there, {greetings}")
        greeting_header.setFont(QFont('Arial', 15))
        greeting_and_lbl_today_layout.addWidget(greeting_header)

        # Show date today
        label_today = QLabel(f"Today is {current_date}")
        label_today.setFont(QFont('Arial', 9))
        greeting_and_lbl_today_layout.addWidget(label_today, alignment=Qt.AlignRight)

        # add the greeting_and_lbl_today_layout layout to the main layout
        self.layout().addLayout(greeting_and_lbl_today_layout)

        # create a QLabel object to display the time
        self.lbl_current_time = QLabel(self)
        self.lbl_current_time.setFont(QFont('Arial', 9))
        self.layout().addWidget(self.lbl_current_time, alignment=Qt.AlignTop | Qt.AlignRight)

        # start the timer to update the label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # update every 1 second

        # Draw a horizontal line -----------------------------------------------------------------------------
        self.layout().addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Customer form header
        cust_header = QLabel("Customer Form")
        cust_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header, alignment=Qt.AlignCenter)

        #########################################################################
        # BUTTONS
        #########################################################################
        # Set style for layouts
        style_sheet_style = "QPushButton { text-align: center; }"

        # Create the button layout
        cust_buttons_layout = QHBoxLayout()

        # Create a button to open the other user form
        cust_entry_button = QPushButton(clicked=lambda: self.open_addnew_custwindow())
        cust_entry_icon = QIcon(icons_dir + "add_new_customer.png")
        cust_entry_button.setIcon(cust_entry_icon)
        cust_entry_button.setIconSize(QSize(50, 50))  # Adjust the icon size as needed
        cust_entry_button.setFixedSize(150, 80)  # Set the desired button size

        # Set the button text alignment to center
        cust_entry_button.setStyleSheet(style_sheet_style)

        # Create a QVBoxLayout for the button
        cust_entry_layout = QVBoxLayout()
        cust_entry_layout.addWidget(cust_entry_button, alignment=Qt.AlignHCenter)
        cust_entry_layout.addWidget(QLabel("Add New Customer", alignment=Qt.AlignHCenter))

        # Create a QWidget for the button layout
        cust_entry_widget = QWidget()
        cust_entry_widget.setLayout(cust_entry_layout)

        # Add the button widget to the main layout
        cust_buttons_layout.addWidget(cust_entry_widget, alignment=Qt.AlignCenter)

        # Create a button to edit customer information
        cust_edit_button = QPushButton(clicked=lambda: self.open_edit_custwindow())
        edit_customer_icon = QIcon(icons_dir + "edit_customer.png")
        cust_edit_button.setIcon(edit_customer_icon)
        cust_edit_button.setIconSize(QSize(50, 50))  # Adjust the icon size as needed
        cust_edit_button.setFixedSize(150, 80)  # Set the desired button size

        # Set the button text alignment to center
        cust_edit_button.setStyleSheet(style_sheet_style)

        # Create a QVBoxLayout for the button
        cust_edit_layout = QVBoxLayout()
        cust_edit_layout.addWidget(cust_edit_button, alignment=Qt.AlignHCenter)
        cust_edit_layout.addWidget(QLabel("Edit Customer Information", alignment=Qt.AlignHCenter))

        # Create a QWidget for the button layout
        cust_edit_widget = QWidget()
        cust_edit_widget.setLayout(cust_edit_layout)

        # Add the button widget to the main layout
        cust_buttons_layout.addWidget(cust_edit_widget, alignment=Qt.AlignCenter)

        # Add the buttons layout to the main layout
        self.layout().addLayout(cust_buttons_layout)

        # Draw a horizontal line -----------------------------------------------------------------------------
        self.layout().addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Ticket form header
        ticket_form_header = QLabel("Ticket Form")
        ticket_form_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(ticket_form_header, alignment=Qt.AlignCenter)

        # Create the button layout
        ts_app_buttons_layout = QHBoxLayout()

        # call aharts_ticket_entry.py
        ticket_entry_button = QPushButton(clicked = lambda: self.open_create_service_ticketwindow())
        service_ticket_icon = QIcon(icons_dir+"service_ticket.png")
        ticket_entry_button.setIcon(service_ticket_icon)
        ticket_entry_button.setIconSize(QSize(50, 50))  # Adjust the icon size as needed
        ticket_entry_button.setFixedSize(150, 80)  # Set the desired button size

        # Set the button text alignment to center
        ticket_entry_button.setStyleSheet(style_sheet_style)

        # Create a QVBoxLayout for the button
        ticket_entry_layout = QVBoxLayout()
        ticket_entry_layout.addWidget(ticket_entry_button, alignment=Qt.AlignHCenter)
        ticket_entry_layout.addWidget(QLabel("Service Ticket", alignment=Qt.AlignHCenter))

        # Create a QWidget for the button layout
        ticket_entry_widget = QWidget()
        ticket_entry_widget.setLayout(ticket_entry_layout)

        # Add the button widget to the main layout
        ts_app_buttons_layout.addWidget(ticket_entry_widget, alignment=Qt.AlignCenter)

        # Appliance troubleshooting log
        appliance_ts_log = QPushButton(clicked = lambda: self.open_troubleshootingwindow())
        ts_order_icon = QIcon(icons_dir+"troubleshooting_order.png")
        appliance_ts_log.setIcon(ts_order_icon)
        appliance_ts_log.setIconSize(QSize(50, 50))  # Adjust the icon size as needed
        appliance_ts_log.setFixedSize(150, 80)  # Set the desired button size

        # Set the button text alignment to center
        appliance_ts_log.setStyleSheet(style_sheet_style)

        # Create a QVBoxLayout for the button
        appliance_ts_log_layout = QVBoxLayout()
        appliance_ts_log_layout.addWidget(appliance_ts_log, alignment=Qt.AlignHCenter)
        appliance_ts_log_layout.addWidget(QLabel("Appliance Troubleshooting Order", alignment=Qt.AlignHCenter))

        # Create a QWidget for the button layout
        appliance_ts_log_widget = QWidget()
        appliance_ts_log_widget.setLayout(appliance_ts_log_layout)

        # Add the button widget to the main layout
        ts_app_buttons_layout.addWidget(appliance_ts_log_widget, alignment=Qt.AlignCenter)

        # Add the buttons layout to the main layout
        self.layout().addLayout(ts_app_buttons_layout)

        # Draw a horizontal line -----------------------------------------------------------------------------
        self.layout().addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Databases
        database_header = QLabel("Databases")
        database_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(database_header, alignment=Qt.AlignCenter)

        # create a QHBoxLayout to hold the buttons
        #db_buttons_layout = QHBoxLayout()

        # create a QHBoxLayout to hold the buttons
        db_buttons_layout = QHBoxLayout()

        # Open database button
        cust_db_btn = QPushButton("View Customer Database", clicked=lambda: open_cust_database_viewer(self))
        cust_db_icon = QIcon(icons_dir + "customer_database.png")
        cust_db_btn.setIcon(cust_db_icon)
        db_buttons_layout.addWidget(cust_db_btn)

        # Open database button
        serviceticket_db_btn = QPushButton("View Service-Ticket Database", clicked=lambda: open_serviceticket_database_viewer(self))
        serviceticket_db_icon = QIcon(icons_dir + "service_ticket_database.png")
        serviceticket_db_btn.setIcon(serviceticket_db_icon)
        db_buttons_layout.addWidget(serviceticket_db_btn)

        ts_order_db_btn = QPushButton("View Troubleshooting Order Database", clicked=lambda: open_ts_order_database_viewer(self))
        ts_order_db_icon = QIcon(icons_dir + "troubleshooting.png")
        ts_order_db_btn.setIcon(ts_order_db_icon)
        db_buttons_layout.addWidget(ts_order_db_btn)

        # add the QHBoxLayout to the main layout
        self.layout().addLayout(db_buttons_layout)

        
        # refresh page
        reload_button = QPushButton("RELOAD PAGE", clicked = lambda: reload_main())
        reload_button.setFont(QFont('Arial', 15))
        self.layout().addWidget(reload_button)
        
        
        ########################################################
        # FUNCTIONS
        ########################################################
        def reload_main():
            # Close the existing main form by quitting the application
            app.quit()
            # Restart the application
            subprocess.Popen([sys.executable, __file__])
 
    def open_addnew_custwindow(self):
        # Show the customer form and hide the main form 
        addnew_custwindow = AddNewCustWindow(self)
        addnew_custwindow.show()
        self.hide()

    def open_edit_custwindow(self):
        self.edit_custwindow = Edit_CustWindow(self)
        self.edit_custwindow.show()
        self.hide()
        
    def open_create_service_ticketwindow(self):       
        self.create_service_ticketwindow = ServiceTicketWindow(self,null)
        self.create_service_ticketwindow.show()
        self.hide()
       
    def open_troubleshootingwindow(self):
        self.troubleshootingwindow = TroubleshootingWindow(self,null)
        self.troubleshootingwindow.show()
        self.hide()
                 
    # This code updates lbl_current_time every seconds  
    def update_time(self):
        # get the current time as a string
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        # update the text property of the existing QLabel object
        self.lbl_current_time.setText(current_time)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Close Application",
            "Are you sure you want to close the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

try:

    # Main application
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        main_form = MainForm()
        main_form.show()
        sys.exit(app.exec_())

except Exception as e:
    # Log the exception message and traceback
    QMessageBox.information(None, "AHARTS", default_err_msg)
    error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
    log_message(error_message)
