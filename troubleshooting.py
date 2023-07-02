from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyperclip

# Customize scripts
from database_viewer import *
from backend.logs_generator import *
from backend.public_backend import *
from backend.goto_page import return_to_previous_page
from backend.troubleshooting_backend import *

class TroubleshootingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("AHARTS - Troubleshooting")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowIcon(QtGui.QIcon(tsystem_icon()))

        # Store a reference to the main form
        self.main_window = main_window
        
        # Header
        header = QtWidgets.QLabel("Anthony's Home Appliance-Repair Ticketing System")
        header.setFont(QtGui.QFont('Arial', 25))
        self.layout.addWidget(header)

        # Troubleshooting information section
        troubleshoot_header = QtWidgets.QLabel("Troubleshooting Information:")
        troubleshoot_header.setFont(QtGui.QFont('Arial', 15))
        self.layout.addWidget(troubleshoot_header)

        form_layout = QtWidgets.QFormLayout()

        # Service Ticket Number
        serv_ticket = QtWidgets.QLabel("Service-Ticket Number:")
        serv_ticket.setFont(QtGui.QFont('Arial', 9))
        serv_ticket_entry = QtWidgets.QLineEdit()
        serv_ticket_entry.setPlaceholderText("Input Service-Ticket number here...")
        serv_ticket_entry.setText(pyperclip.paste())
        form_layout.addRow(serv_ticket, serv_ticket_entry)

        self.layout.addLayout(form_layout)

        # What's customer full name label
        cust_ticket_lbl = QtWidgets.QLabel("What's the customer Service-Ticket number?")
        cust_ticket_lbl.setFont(QtGui.QFont('Arial', 12))
        self.layout.addWidget(cust_ticket_lbl)

        # Customer information for this ticket
        cust_info_lbl = QtWidgets.QLabel("Customer Name: Ipsum Dolor")
        cust_info_lbl.setFont(QtGui.QFont('Arial', 12))
        self.layout.addWidget(cust_info_lbl)

        # Textbox placeholders
        service_info = QtWidgets.QComboBox()
        service_info.addItems([service.strip() for service in services()])

        broken_comp_txtbox = QtWidgets.QLineEdit()
        broken_comp_txtbox.setPlaceholderText("Fuse, Wiring, Capacitor etc.")

        quantity_txtbox = QtWidgets.QLineEdit()
        quantity_txtbox.setPlaceholderText("Number only (1, 2, 10)")

        price_txtbox = QtWidgets.QLineEdit()
        price_txtbox.setPlaceholderText("Number only (50, 150, 300)")

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(QtWidgets.QLabel("Type of Service:"), service_info)
        form_layout.addRow(QtWidgets.QLabel("Broken Component:"), broken_comp_txtbox)
        form_layout.addRow(QtWidgets.QLabel("Quantity:"), quantity_txtbox)
        form_layout.addRow(QtWidgets.QLabel("Price:"), price_txtbox)

        self.layout.addLayout(form_layout)

        # Buttons to modify data in table
        add_button = QtWidgets.QPushButton("Add")
        add_button.clicked.connect(lambda: add_data(service_info.currentText(), broken_comp_txtbox.text(), quantity_txtbox.text(), price_txtbox.text(), table_widget))

        remove_button = QtWidgets.QPushButton("Remove")
        remove_button.clicked.connect(lambda: remove_data(table_widget))

        # Create a layout for the buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)

        # Add the layout with buttons to the form layout
        form_layout.addRow(buttons_layout)

        # Create a table widget to display the transferred data with column headers
        table_widget = QtWidgets.QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Service", "Broken Component", "Quantity", "Price"])

        # Set the column resize mode to stretch
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.layout.addWidget(table_widget)

        # Add Data inside the Table
        def add_data(service, broken_component, quantity, price, table_widget):
            row_count = table_widget.rowCount()
            table_widget.insertRow(row_count)
            table_widget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(service))
            table_widget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(broken_component))
            table_widget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(quantity))
            table_widget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(price))

        # Remove Data inside the Table
        def remove_data(table_widget):
            selected_row = table_widget.currentRow()
            if selected_row >= 0:
                table_widget.removeRow(selected_row)

        #########################################################################
        # BUTTONS
        #########################################################################

        # Draw a horizontal line
        self.layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save")
        buttons_layout.addWidget(save_button)

        # Clear all fields buttonl
        clear_button = QPushButton("Clear All")
        buttons_layout.addWidget(clear_button)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Open database button
        serviceticket_db_btn = QPushButton("View Service-Ticket Database", clicked = lambda: open_serviceticket_database_viewer(self))
        buttons_layout.addWidget(serviceticket_db_btn)

        # Go back to main page
        goback_btn = QPushButton("Go Back", clicked = lambda: return_to_previous_page(self, main_window))
        buttons_layout.addWidget(goback_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        self.show()

        # Removing clipboard history
        pyperclip.copy('')

    def closeEvent(self, event):
        return_to_previous_page(self, self.main_window)

'''
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = TroubleshootingWindow()
    sys.exit(app.exec_())'''
