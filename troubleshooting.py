import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import pyperclip
import sys

# Customize scripts
from database_viewer import *
from logs_generator import *
from public_backend import *
from goto_page import *
from troubleshooting_backend import *

class TroubleshootingWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AHARTS - Troubleshooting")
        self.layout = qtw.QVBoxLayout(self)

        # Header
        header = qtw.QLabel("Anthony's Home Appliance-Repair Ticketing System")
        header.setFont(qtg.QFont('Arial', 25))
        self.layout.addWidget(header)

        # Troubleshooting information section
        troubleshoot_header = qtw.QLabel("Troubleshooting Information:")
        troubleshoot_header.setFont(qtg.QFont('Arial', 15))
        self.layout.addWidget(troubleshoot_header)

        form_layout = qtw.QFormLayout()

        # Service Ticket Number
        serv_ticket = qtw.QLabel("Service-Ticket Number:")
        serv_ticket.setFont(qtg.QFont('Arial', 9))
        serv_ticket_entry = qtw.QLineEdit()
        serv_ticket_entry.setPlaceholderText("Input Service-Ticket number here...")
        serv_ticket_entry.setText(pyperclip.paste())
        form_layout.addRow(serv_ticket, serv_ticket_entry)

        self.layout.addLayout(form_layout)

        # What's customer full name label
        cust_ticket_lbl = qtw.QLabel("What's the customer Service-Ticket number?")
        cust_ticket_lbl.setFont(qtg.QFont('Arial', 12))
        self.layout.addWidget(cust_ticket_lbl)

        # Customer information for this ticket
        cust_info_lbl = qtw.QLabel("Customer Name: Ipsum Dolor")
        cust_info_lbl.setFont(qtg.QFont('Arial', 12))
        self.layout.addWidget(cust_info_lbl)

        # Textbox placeholders
        service_info = qtw.QComboBox()
        service_info.addItems([service.strip() for service in services()])

        broken_comp_txtbox = qtw.QLineEdit()
        broken_comp_txtbox.setPlaceholderText("Fuse, Wiring, Capacitor etc.")

        quantity_txtbox = qtw.QLineEdit()
        quantity_txtbox.setPlaceholderText("Number only (1, 2, 10)")

        price_txtbox = qtw.QLineEdit()
        price_txtbox.setPlaceholderText("Number only (50, 150, 300)")

        form_layout = qtw.QFormLayout()
        form_layout.addRow(qtw.QLabel("Type of Service:"), service_info)
        form_layout.addRow(qtw.QLabel("Broken Component:"), broken_comp_txtbox)
        form_layout.addRow(qtw.QLabel("Quantity:"), quantity_txtbox)
        form_layout.addRow(qtw.QLabel("Price:"), price_txtbox)

        self.layout.addLayout(form_layout)

        # Buttons to modify data in table
        add_button = qtw.QPushButton("Add")
        add_button.clicked.connect(lambda: add_data(service_info.currentText(), broken_comp_txtbox.text(), quantity_txtbox.text(), price_txtbox.text(), table_widget))

        remove_button = qtw.QPushButton("Remove")
        remove_button.clicked.connect(lambda: remove_data(table_widget))

        # Create a layout for the buttons
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)

        # Add the layout with buttons to the form layout
        form_layout.addRow(buttons_layout)

        # Create a table widget to display the transferred data with column headers
        table_widget = qtw.QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Service", "Broken Component", "Quantity", "Price"])

        # Set the column resize mode to stretch
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.Stretch)

        self.layout.addWidget(table_widget)

        # Add Data inside the Table
        def add_data(service, broken_component, quantity, price, table_widget):
            row_count = table_widget.rowCount()
            table_widget.insertRow(row_count)
            table_widget.setItem(row_count, 0, qtw.QTableWidgetItem(service))
            table_widget.setItem(row_count, 1, qtw.QTableWidgetItem(broken_component))
            table_widget.setItem(row_count, 2, qtw.QTableWidgetItem(quantity))
            table_widget.setItem(row_count, 3, qtw.QTableWidgetItem(price))

        # Remove Data inside the Table
        def remove_data(table_widget):
            selected_row = table_widget.currentRow()
            if selected_row >= 0:
                table_widget.removeRow(selected_row)

        # BUTTONS ##########################################################################################

        # Save button
        cust_save_button = qtw.QPushButton("Save")
        self.layout.addWidget(cust_save_button)

        # Clear all fields button
        cust_clear_button = qtw.QPushButton("Clear All")
        self.layout.addWidget(cust_clear_button)

        # Open database button
        cust_db_button = qtw.QPushButton("View Customer Database")
        self.layout.addWidget(cust_db_button)

        # Back to Main button
        to_main_button = qtw.QPushButton("Back to Main")
        self.layout.addWidget(to_main_button)

        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = TroubleshootingWindow()
    sys.exit(app.exec_())
