# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
from database_viewer import *
from backend.logs_generator import *
from backend.goto_page import return_to_previous_page
from backend.troubleshooting_backend import *

class TroubleshootingWindow(QWidget):
    def __init__(self, main_window, recent_txn_id):
        super().__init__()
        self.setWindowTitle("AHARTS - Troubleshooting Order")
        self.layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon(tsystem_icon))

        # Store a reference to the main form
        self.main_window = main_window
        self.recent_txn_id = str(recent_txn_id)

        # Check if Troubleshooting database exist
        check_troubleshooting_order_db()

        # Look for customer information based on tracking number
        def look_up_order_information():
            service_ticket_id = validate_num_text(serv_ticket_input)
            
            try:
                cust_tracking_id = int(look_up_cust_tracking_id(service_ticket_id))
                cust_info_lbl.setText(f"Customer Name: <b>{look_up_cust_name(cust_tracking_id)}</b>")      
            except:
                cust_info_lbl.setText("Customer Name: <b>No Information Found</b>")
                pass

            # Appliance for inputted service id
            appliance_info_lbl.setText(f"Appliance: <b>{look_up_appliance(service_ticket_id)}</b>")

            # Load Troubleshooting order based on service_ticket_id
            data_rows = look_up_ts_order_data(service_ticket_id)

            # Clear the table widget
            table_widget.clearContents()
            table_widget.setRowCount(0)

            # Update the table_widget with the retrieved data
            for i, row in enumerate(data_rows.itertuples(index=False)):
                table_widget.insertRow(i)
                for j, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    table_widget.setItem(i, j, item)

            
        # Header
        main_header = QLabel(my_main_header)
        main_header.setFont(QFont('Arial', 20))
        self.layout.addWidget(main_header)

        # Troubleshooting information section
        troubleshoot_header = QLabel("Troubleshooting Information:")
        troubleshoot_header.setFont(QFont('Arial', 15))
        self.layout.addWidget(troubleshoot_header)

        form_layout = QFormLayout()

        # Service Ticket Number
        serv_ticket = QLabel("Service-Ticket Number:")
        serv_ticket.setFont(QFont('Arial', 9))
        serv_ticket_input = QLineEdit()
        serv_ticket_input.setPlaceholderText("Input Service-Ticket number here...")
        serv_ticket_input.textChanged.connect(look_up_order_information)
        form_layout.addRow(serv_ticket, serv_ticket_input)

        self.layout.addLayout(form_layout)

        # Customer information for this ticket
        cust_info_lbl = QLabel("Customer name will appear here")
        cust_info_lbl.setFont(QFont('Arial', 12))
        self.layout.addWidget(cust_info_lbl)

        # Customer information for this ticket
        appliance_info_lbl = QLabel("Customer appliance will appear here")
        appliance_info_lbl.setFont(QFont('Arial', 12))
        self.layout.addWidget(appliance_info_lbl)

        # Textbox placeholders
        service_info = QComboBox()
        service_info.addItems([service.strip() for service in services()])

        broken_comp_txtbox = QLineEdit()
        broken_comp_txtbox.setPlaceholderText("Fuse, Wiring, Capacitor etc.")

        quantity_txtbox = QLineEdit()
        quantity_txtbox.setPlaceholderText("Number only (1, 2, 10)")
        quantity_txtbox.textChanged.connect(lambda: validate_num_text(quantity_txtbox))

        price_txtbox = QLineEdit()
        price_txtbox.setPlaceholderText("Number only (50, 150, 300)")
        price_txtbox.textChanged.connect(lambda: validate_num_text(price_txtbox))

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Type of Service:"), service_info)
        form_layout.addRow(QLabel("Broken Component:"), broken_comp_txtbox)
        form_layout.addRow(QLabel("Quantity:"), quantity_txtbox)
        form_layout.addRow(QLabel("Price:"), price_txtbox)

        self.layout.addLayout(form_layout)

        # Grand total label
        grand_total_lbl = QLabel("Grand Total:")
        grand_total_lbl.setFont(QFont('Arial', 10, QFont.Bold))
        actual_grand_total_lbl = QLabel("Php 0.0")
        actual_grand_total_lbl.setFont(QFont('Arial', 10, QFont.Bold))

        # Set the stylesheet with all the styles
        actual_grand_total_lbl.setStyleSheet("background-color: #10752f; color: white; border: 1px solid black; padding: 2px; font-size: 14px; font-weight: bold;")


        # Grand Total button for table widget subtotal column
        grand_total_button = QPushButton("Compute")
        abacus_icon = QIcon(icons_dir+"abacus.png")
        grand_total_button.setIcon(abacus_icon)
        grand_total_button.clicked.connect(lambda: grand_total())


        # Buttons to modify data in table
        add_button = QPushButton("Add")
        add_icon = QIcon(icons_dir+"addition_operator.png")
        add_button.setIcon(add_icon)
        add_button.clicked.connect(lambda: add_data(service_info.currentText(), broken_comp_txtbox.text(), quantity_txtbox.text(), price_txtbox.text(), table_widget))

        remove_button = QPushButton("Remove")
        subtract_icon = QIcon(icons_dir+"subtract_operator.png")
        remove_button.setIcon(subtract_icon)
        remove_button.clicked.connect(lambda: remove_data(table_widget))

        # Create a layout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(grand_total_lbl)
        buttons_layout.addWidget(actual_grand_total_lbl)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(grand_total_button)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(remove_button)

        # Add the layout with buttons to the form layout
        form_layout.addRow(buttons_layout)  

        # Create a table widget to display the transferred data with column headers
        table_widget = QTableWidget()
        table_widget.setColumnCount(6)
        table_widget.setHorizontalHeaderLabels(["Order ID"]+table_widget_headers)

        # Set the column width for the order ID column
        table_widget.setColumnWidth(0, 100)  # Adjust the width as needed

        # Set the column alignment for the order ID column
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Set the column resize mode to stretch for other columns
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(table_widget)

        # Add Data inside the Table
        def add_data(service, broken_component, quantity, price, table_widget):
            # Check first if Service-Ticket ID exist
            service_ticket_id = validate_num_text(serv_ticket_input) 
            cust_tracking_id = look_up_cust_tracking_id(service_ticket_id)
            if cust_tracking_id:
            # Generate order id for each order
                order_id = generate_order_id(table_widget)

                row_count = table_widget.rowCount()
                table_widget.insertRow(row_count)

                table_widget.setItem(row_count, 0, QTableWidgetItem(str(order_id)))
                table_widget.setItem(row_count, 1, QTableWidgetItem(service))
                table_widget.setItem(row_count, 2, QTableWidgetItem(broken_component))
                table_widget.setItem(row_count, 3, QTableWidgetItem(quantity))
                table_widget.setItem(row_count, 4, QTableWidgetItem(price))

                subtotal = compute_subtotal(quantity, price)
                subtotal_item = QTableWidgetItem(str(subtotal))
                table_widget.setItem(row_count, 5, subtotal_item)

                broken_comp_txtbox.clear()
                quantity_txtbox.clear()
                price_txtbox.clear()

                grand_total()

        def grand_total():
            #actual_grand_total_lbl.show
            actual_grand_total_lbl.setText(compute_grand_total(table_widget))

        # Remove Data inside the Table
        def remove_data(table_widget):
            selected_row = table_widget.currentRow()
            if selected_row >= 0:
                table_widget.removeRow(selected_row)
                grand_total()

        # Draw a horizontal line
        self.layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        #########################################################################
        # BUTTONS
        #########################################################################

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save", clicked = lambda: save_it())
        buttons_layout.addWidget(save_button)

        # Clear all fields buttonl
        clear_button = QPushButton("Clear All", clicked = lambda: clear_all())
        buttons_layout.addWidget(clear_button)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        # create a QHBoxLayout to hold the buttons
        buttons_layout = QHBoxLayout()

        # Open database button
        serviceticket_db_btn = QPushButton("View Troubleshooting Order Database", clicked = lambda: open_ts_order_database_viewer(self))
        buttons_layout.addWidget(serviceticket_db_btn)

        # Go back to main page
        goback_btn = QPushButton("Go Back", clicked = lambda: return_to_previous_page(self, main_window))
        buttons_layout.addWidget(goback_btn)

        # add the buttons layout to the main layout
        self.layout.addLayout(buttons_layout)

        self.show()


        ########################################################
        # FUNCTIONS
        ########################################################

        def save_it():
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AHARTS")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(QMessageBox)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                # Parse the service_ticket_id as Text
                service_ticket_id = serv_ticket_input.text()
                cust_tracking_id = look_up_cust_tracking_id(validate_num_text(serv_ticket_input))

                # proceed saving
                save_ts_order(table_widget,service_ticket_id,cust_tracking_id)

                # Clean widgets
                clear_all()

        
        def clear_all():
            serv_ticket_input.clear()
            broken_comp_txtbox.clear()
            quantity_txtbox.clear()
            price_txtbox.clear()
            table_widget.clearContents()
            table_widget.setRowCount(0)
            grand_total_lbl.setText("Grand Total:")
            cust_info_lbl.setText("Customer name will appear here")
            appliance_info_lbl.setText("Customer appliance will appear here")
            grand_total()

        # Parse recent transaction number
        serv_ticket_input.setText(self.recent_txn_id)

    # Beutifications/Extras
    def enterEvent(self, event):
        tooltip_text = 'From the order table, double-click on the cell you want to edit.'
        QToolTip.showText(event.globalPos(), tooltip_text)

    def leaveEvent(self, event):
        QToolTip.hideText()

    def closeEvent(self, event):
        return_to_previous_page(self, self.main_window)


# ...

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = TroubleshootingWindow()
    sys.exit(app.exec_())'''
