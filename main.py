# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
# Sub-pages
from add_new_cust import AddNewCustWindow
from edit_customer import Edit_CustWindow
from create_service_ticket import ServiceTicketWindow
from troubleshooting import TroubleshootingWindow
from receipt import open_receipt

# Backend scripts
from database_viewer import *
from backend.logs_generator import *
from backend.main_backend import *

# Param checker and preparations
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

username = getpass.getuser()

# Simply null
null = ""


# SPLASH SCREEN 
def show_splash_screen(width, height):
    # Create a splash screen widget
    splash = QWidget()
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setWindowTitle("tsystem")
    splash.setWindowIcon(QIcon(tsystem_icon))

    # Create a QLabel to display the animated GIF
    splash_label = QLabel(splash)
    splash_label.setAlignment(Qt.AlignCenter)
    movie = QMovie(splash_gif)  # Replace "animation.gif" with the path to your animated GIF
    movie.frameChanged.connect(lambda frame: splash_label.setPixmap(movie.currentPixmap()))
    movie.start()

    # Calculate the position and size of the splash screen
    desktop = QDesktopWidget().screenGeometry()
    x = desktop.width() // 2 - width // 2
    y = desktop.height() // 2 - height // 2
    splash.setGeometry(x, y, width, height)

    # Show the splash screen
    splash.show()

    return splash, movie

# MainWindow Form
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

        # Create a QHBoxLayout to hold the username and current time labels
        username_currenttime_layout = QHBoxLayout()

        # Create the label to display the current user
        current_user = QLabel(f'Login as: {username}')
        current_user.setFont(QFont('Arial', 9))
        username_currenttime_layout.addWidget(current_user)

        # Create the label to display the current time
        self.lbl_current_time = QLabel(self)
        self.lbl_current_time.setFont(QFont('Arial', 9))
        username_currenttime_layout.addStretch(1)  # Add a stretchable space to push the labels to the right
        username_currenttime_layout.addWidget(self.lbl_current_time)

        # Add the QHBoxLayout to the main layout
        self.layout().addLayout(username_currenttime_layout)

        # Start the timer to update the label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # Update every 1 second

        # Draw a horizontal line -----------------------------------------------------------------------------
        self.layout().addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Customer form header
        cust_header = QLabel("Customer Form")
        cust_header.setFont(QFont('Arial', 15))
        self.layout().addWidget(cust_header, alignment=Qt.AlignCenter)

        #########################################################################
        # BUTTONS
        #########################################################################
        # Set style for buttons layouts
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

        receipt_btn = QPushButton("receipt", clicked = lambda: open_receipt(self))
        receipt_btn.setFont(QFont('Arial', 15))
        self.layout().addWidget(receipt_btn)

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

    app = QApplication(sys.argv)

    # Set the desired dimensions for the splash screen
    splash_width = 500
    splash_height = 470

    # Show the splash screen
    splash, movie = show_splash_screen(splash_width, splash_height)

    # Delay the appearance of the MainWindow
    main_window_delay = QTimer()
    main_window_delay.setInterval(2000)  # Adjust the delay as needed (in milliseconds)

    def show_main_window():
        main_form = MainForm()
        main_form.show()
        main_window_delay.stop()
        splash.close()

    main_window_delay.timeout.connect(show_main_window)
    main_window_delay.start()

    sys.exit(app.exec_())

except Exception as e:
    # Log the exception message and traceback
    QMessageBox.information(None, "AHARTS", default_err_msg)
    error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
    log_message(error_message)
