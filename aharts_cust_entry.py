# Anthony's Home Appliance Repair Ticketing System
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # System userform title
        self.setWindowTitle("AHARTS")
        # Userform layout
        self.setLayout(qtw.QVBoxLayout())

        # Userform header
        uf_header = qtw.QLabel("Anthony's Home Appliance Repair Ticketing System")
        uf_header.setFont(qtg.QFont('Arial', 25))
        self.layout().addWidget(uf_header)

        # Userform header Customer Information
        uf_cust_info = qtw.QLabel("Customer Information: ")
        uf_cust_info.setFont(qtg.QFont('Arial', 15))
        self.layout().addWidget(uf_cust_info)

        # Userform header Customer First Name
        uf_cust_fname = qtw.QLabel("First Name: ")
        uf_cust_fname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_fname)

        # Userform Entry box for customer First Name
        uf_cust_fname_entry = qtw.QLineEdit()
        uf_cust_fname_entry.setObjectName("fname_field")
        self.layout().addWidget(uf_cust_fname_entry)

        # Userform header Customer Last Name
        uf_cust_lname = qtw.QLabel("Last Name: ")
        uf_cust_lname.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_lname)

        # Userform Entry box for customer Last Name
        uf_cust_lname_entry = qtw.QLineEdit()
        uf_cust_lname_entry.setObjectName("lname_field")
        self.layout().addWidget(uf_cust_lname_entry)

        # Userform header Customer Contact Number
        uf_cust_cnum = qtw.QLabel("Contact Number: ")
        uf_cust_cnum.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_cnum)

        # Userform Entry box for customer Contact Number
        uf_cust_cnum_entry = qtw.QLineEdit()
        uf_cust_cnum_entry.setObjectName("cnum_field")
        uf_cust_cnum_entry.setText("+63-917-123-1234")
        self.layout().addWidget(uf_cust_cnum_entry)

        # Userform header Customer Email Address
        uf_cust_Email = qtw.QLabel("Email Address: ")
        uf_cust_Email.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_Email)

        # Userform Entry box for customer Email Address
        uf_cust_Email_entry = qtw.QLineEdit()
        uf_cust_Email_entry.setObjectName("Email_field")
        uf_cust_Email_entry.setText("username@domain.com")
        self.layout().addWidget(uf_cust_Email_entry)

        # Userform header Customer Home Address
        uf_cust_Hadd = qtw.QLabel("Home Address: ")
        uf_cust_Hadd.setFont(qtg.QFont('Arial', 9))
        self.layout().addWidget(uf_cust_Hadd)

        # Userform Entry box for customer Home Address
        uf_cust_Hadd_entry = qtw.QLineEdit()
        uf_cust_Hadd_entry.setObjectName("Hadd_field")
        uf_cust_Hadd_entry.setText("Home# Street Name, Barangay, City Name Province Zip Code")
        self.layout().addWidget(uf_cust_Hadd_entry)

        # Save button
        uf_cust_save_button = qtw.QPushButton("Save", clicked = lambda: save_it())
        self.layout().addWidget(uf_cust_save_button)

        # Clear all fields button
        uf_cust_clear_button = qtw.QPushButton("Clear All", clicked = lambda: clear_all())
        self.layout().addWidget(uf_cust_clear_button)

        # This part is very IMPORTANT!!
        self.show()

        def save_it():
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Question)
            msgBox.setText("Are you sure you want to save changes?")
            msgBox.setWindowTitle("AARTS")
            msgBox.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(qtw.QMessageBox)

            returnValue = msgBox.exec()
            if returnValue == qtw.QMessageBox.Ok:
                print('OK clicked')

        def clear_all():
            uf_cust_fname_entry.setText("")
            uf_cust_lname_entry.setText("")
            uf_cust_cnum_entry.setText("+63-917-123-1234")
            uf_cust_Email_entry.setText("username@domain.com")
            uf_cust_Hadd_entry.setText("Home# Street Name, Barangay, City Name Province Zip Code")
            print("Customer fields has been reset")
            


app = qtw.QApplication([])
mw = MainWindow()

app.exec_()