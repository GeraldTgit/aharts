
from backend.public_backend import *
from backend.receipt_backend import *
from backend.troubleshooting_backend import look_up_ts_order_data


def open_receipt(self,recent_txn_id):
    receipt_window = ReceiptForm(recent_txn_id)
    receipt_window.setGeometry(self.geometry().x() - 200, self.geometry().y(), 200, 500)
    receipt_window.show()


class ReceiptForm(QMainWindow):
    def __init__(self, recent_txn_id):
        super().__init__()
        self.setWindowTitle('Print Receipt')
        self.setWindowIcon(QIcon(tsystem_icon))

        # Create a main widget and set it as the central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Recently saved transaction number
        self.recent_txn_id = str(recent_txn_id)

        # Create a layout for the main widget
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Add a label for the receipt header
        header_label = QLabel(header_line_1)
        header_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(header_label, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel(header_line_2), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel(header_line_3), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel(header_line_4), alignment=Qt.AlignCenter)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        layout.addWidget(QLabel(header_line_5), alignment=Qt.AlignCenter)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        form_layout = QFormLayout()

        # Service Ticket Number
        serv_ticket = QLabel("Service-Ticket #:")
        self.serv_ticket_input = QLineEdit()
        self.serv_ticket_input.setPlaceholderText("Input Service-Ticket number here...")
        self.serv_ticket_input.textChanged.connect(self.look_up_order_information)
        self.serv_ticket_input.setFixedWidth(50)
        self.serv_ticket_input.setFixedHeight(20)
        form_layout.addRow(serv_ticket, self.serv_ticket_input)

        layout.addLayout(form_layout)

        self.cust_name = QLabel("Customer Name:")
        layout.addWidget(self.cust_name)

        self.cust_appliance = QLabel("Appliance:")
        layout.addWidget(self.cust_appliance)

        self.appliance_issue = QLabel("Issue:")
        layout.addWidget(self.appliance_issue)
        
        self.printed_date = QLabel("")
        layout.addWidget(self.printed_date)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        self.total_amount = 0

        self.ts_form_layout = QFormLayout()

        # Troubleshooting labels
        item_label = QLabel("Service:")
        qty_label = QLabel("Quantity:")
        price_label = QLabel("Price:")
        subtotal_label = QLabel("Subtotal:")

        # Create a layout for troubleshooting labels
        ts_layout = QHBoxLayout()
        ts_layout.addWidget(item_label)
        ts_layout.addWidget(qty_label)
        ts_layout.addWidget(price_label)
        ts_layout.addWidget(subtotal_label)

        # Add the layout with troubleshooting labels to the form layout
        self.ts_form_layout.addRow(ts_layout)

        layout.addLayout(self.ts_form_layout)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        # Footer line
        layout.addWidget(QLabel(footer))

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        buttons_form_layout = QFormLayout()

        buttons_layout = QHBoxLayout()
        print_button = QPushButton("PRINT", clicked=lambda: self.print_receipt())
        close_button = QPushButton("CLOSE", clicked=lambda: self.hide())
        buttons_layout.addWidget(print_button)
        buttons_layout.addWidget(close_button)

        buttons_form_layout.addRow(buttons_layout)

        layout.addLayout(buttons_form_layout)

        # Parsing the recent transaction saved
        self.serv_ticket_input.setText(self.recent_txn_id)

    def look_up_order_information(self):
        service_ticket_id = validate_num_text(self.serv_ticket_input)

        try:
            cust_tracking_id = int(look_up_cust_tracking_id(service_ticket_id))
            self.cust_name.setText(f"Customer Name: <b>{look_up_cust_name(cust_tracking_id)}</b>")
        except:
            self.cust_name.setText("Customer Name: <b>No Information Found</b>")
            pass

        # Appliance for inputted service id
        self.cust_appliance.setText(f"Appliance: <b>{look_up_appliance(service_ticket_id)}</b>")

        self.appliance_issue.setText(f"Issue: <b>{look_up_issue(service_ticket_id)}</b>")

        # Load Troubleshooting order based on service_ticket_id
        data = look_up_ts_order_data(service_ticket_id)
        self.init_layout(data)
    
    
    def init_layout(self, data):    
        # Clear the existing items in the layout
        while self.ts_form_layout.rowCount() > 0:
            self.ts_form_layout.removeRow(0)

        self.total_amount = 0

        grouped_data = data.groupby('Service')

        # Add labels for item details
        for service, group in grouped_data:
            # Create a new custom widget to combine QVBoxLayout and QFormLayout
            service_widget = QWidget()
            service_layout = QVBoxLayout(service_widget)

            # Create a QLabel to display the service name
            service_data = QLabel(service)
            service_layout.addWidget(service_data)

            # Create a new QFormLayout for troubleshooting labels
            ts_form_layout = QFormLayout()
            for index, row in group.iterrows():  # <- Iterate over group, not entire data
                # Troubleshooting labels
                broken_component = QLabel(row['Component'])

                try:
                    quantity = int(row['Quantity'])
                except ValueError:
                    quantity = 1

                try:
                    price = float(row['Price'])
                except ValueError:
                    price = 0.0

                qty_data = QLabel(str(quantity))
                try:
                    price_data = QLabel(f"{price:.2f}")
                except ValueError:
                    price_data = QLabel("Invalid Price")

                item_total = quantity * price
                subtotal_data = QLabel(f"{item_total:.2f}")

                # Create a layout for troubleshooting labels
                ts_layout = QHBoxLayout()
                ts_layout.addWidget(broken_component)
                ts_layout.addWidget(qty_data)
                ts_layout.addWidget(price_data)
                ts_layout.addWidget(subtotal_data)

                # Add the layout with troubleshooting labels to the form layout
                ts_form_layout.addRow(ts_layout)

                self.total_amount += item_total

            # Add the ts_form_layout to the service_layout
            service_layout.addLayout(ts_form_layout)

            # Add the service_widget to the main layout
            self.ts_form_layout.addWidget(service_widget)

        # Remove previous total amount label (if any) and add the updated one
        self.grand_total_label = QLabel(f"\nTotal: <b>Php {self.total_amount:.2f}</b>")
        self.grand_total_label.setAlignment(Qt.AlignRight)  # Align the label to the right
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            widget = item.widget()
            if isinstance(widget, QLabel) and "Total: " in widget.text():
                widget.deleteLater()
                break

        self.ts_form_layout.addWidget(self.grand_total_label)  # Add the grand_total_label without alignment


        # Payment # Store the layout for later use
        self.payment_layout = QFormLayout()
        self.payment_label = QLabel("Payment:")
        self.payment_input = QLineEdit()
        self.payment_input.setFixedWidth(50)
        self.payment_input.setFixedHeight(20)
        self.payment_input.textChanged.connect(self.change_amount) # Update Change label when payment is entered
        self.payment_layout.addRow(self.payment_label, self.payment_input)

        right_align_layout = QHBoxLayout()
        right_align_layout.addStretch(1)  # Add empty stretch to push the payment_layout to the right side
        right_align_layout.addLayout(self.payment_layout)
        self.right_align_widget = QWidget()
        self.right_align_widget.setLayout(right_align_layout)

        # Change
        self.change_label = QLabel("")  
        self.change_label.setAlignment(Qt.AlignRight)

        # Add the right_align_widget to the ts_form_layout
        self.ts_form_layout.addWidget(self.right_align_widget)
        # show change_label in the form
        self.ts_form_layout.addWidget(self.change_label)


    def change_amount(self):
        try:
            payment = validate_num_text(self.payment_input)
            change = payment - self.total_amount
            self.change_label.setText(f"Change: <b>Php {change}</b>") 
        except:
            pass

    def print_receipt(self):
        process_dttm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.printed_date.setText(f"Date printed: {process_dttm}")

'''
if __name__ == "__main__":
    # Sample data
    data = ""  # Initialize with empty data
    app = QApplication(sys.argv)
    receipt_form = ReceiptForm(data)
    
    receipt_form.show()
    sys.exit(app.exec())
'''
