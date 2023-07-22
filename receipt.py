
from backend.public_backend import *
from backend.troubleshooting_backend import look_up_ts_order_data

class ReceiptForm(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Receipt')
        self.setGeometry(100, 100, 400, 300)
        self.resize(200, 500)
        self.setWindowIcon(QIcon(tsystem_icon))

        # Create a main widget and set it as the central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Dash line style
        dash_line_style = "border: none; border-bottom: 1px dashed black;"

        # Create a layout for the main widget
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        # Add a label for the receipt header
        header_label = QLabel("Anthony's Home Appliance Repair Shop")
        header_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(header_label, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("#305 Maharlika Highway, La Torre,"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Talavera, Nueva Ecija 3114"), alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Contact #: 09083287926 / 09368505809"), alignment=Qt.AlignCenter)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        layout.addWidget(QLabel('OFFICIAL RECEIPT'), alignment=Qt.AlignCenter)

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

        process_dttm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        layout.addWidget(QLabel(f"Date printed: {process_dttm}"))

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        self.total_amount = 0

        self.ts_form_layout = QFormLayout()

        # Troubleshooting labels
        item_label = QLabel("Trouble:")
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

        # Display the total amount
        layout.addWidget(QLabel(f"\nTotal: <b>Php {self.total_amount:.2f}</b>"), alignment=Qt.AlignRight)

        # Align the form_layout to the right
        form_layout = QFormLayout()

        # Payment
        payment_label = QLabel("Payment:")
        self.payment_input = QLineEdit()
        self.payment_input.setFixedWidth(50)
        self.payment_input.setFixedHeight(20)
        self.payment_input.textChanged.connect(self.change_amount)
        form_layout.addRow(payment_label, self.payment_input)

        self.right_align_layout = QVBoxLayout()
        self.right_align_layout.addStretch()  # Add stretch to push the form_layout to the right side
        self.right_align_layout.addLayout(form_layout)

        right_align_widget = QWidget()
        right_align_widget.setLayout(self.right_align_layout)
        layout.addWidget(right_align_widget, alignment=Qt.AlignRight)  # Align to the right side

        # Display the change amount
        self.change_label = QLabel("")
        layout.addWidget(self.change_label, alignment=Qt.AlignRight)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        layout.addWidget(QLabel('This receipt is generated by the tsystem. tsystem is an\nopen-source software developed by Gerald Dave Trajano\nFor more information, please visit ---\nhttps://github.com/geraldtgit/aharts\nEmail: geralddavetrajano@gamail.com'))

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        buttons_form_layout = QFormLayout()

        buttons_layout = QHBoxLayout()
        print_button = QPushButton("PRINT")
        close_button = QPushButton("CLOSE")
        buttons_layout.addWidget(print_button)
        buttons_layout.addWidget(close_button)

        buttons_form_layout.addRow(buttons_layout)

        layout.addLayout(buttons_form_layout)

    def change_amount(self):
        payment = validate_num_text(self.payment_input)
        try:
            total_amount = self.compute_total_amount()
            change = payment - total_amount
            self.change_label.setText(f"Change: <b>Php {change}</b>")
        except:
            pass

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

    def compute_total_amount(self):
        total_amount = 0
        for index, row in data.iterrows():
            qtty = row['Quantity']
            if row['Quantity'] == 0:
                qtty = 1
            try:
                price = float(row['Price'])
            except ValueError:
                price = 0.0
            item_total = qtty * price
            total_amount += item_total
        return total_amount

    def init_layout(self, data):
        # Clear the existing items in the layout
        while self.ts_form_layout.rowCount() > 0:
            self.ts_form_layout.removeRow(0)

        self.total_amount = 0

        # Add labels for item details
        for index, row in data.iterrows():
            # Troubleshooting labels
            item_data = QLabel(row['Service'])

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
            ts_layout.addWidget(item_data)
            ts_layout.addWidget(qty_data)
            ts_layout.addWidget(price_data)
            ts_layout.addWidget(subtotal_data)

            # Add the layout with troubleshooting labels to the form layout
            self.ts_form_layout.addRow(ts_layout)

            self.total_amount += item_total

        # Display the total amount
        total_label = QLabel(f"\nTotal: <b>Php {self.total_amount:.2f}</b>")
        total_label.setAlignment(Qt.AlignRight)
        self.layout().addWidget(total_label)



if __name__ == "__main__":
    # Sample data
    data = ""  # Initialize with empty data
    app = QApplication(sys.argv)
    receipt_form = ReceiptForm(data)
    receipt_form.show()
    sys.exit(app.exec())
