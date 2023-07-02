import sys
import csv
import psutil
import ctypes
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

# Customize scripts
from backend.logs_generator import *
from backend.public_backend import *

# Task bar icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid())

# Save and closes customer_db in excel application if open
def save_and_close_database(customer_db):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'EXCEL.EXE':
            try:
                process.terminate()
            except psutil.NoSuchProcess:
                pass

    subprocess.call(['taskkill', '/f', '/im', 'EXCEL.EXE'], shell=True)

# Check if the customer.csv file exists in the customer_db() directory
headers = ['Customer ID', 'First Name', 'Last Name', 'Contact Number', 'Email', 'Home Address', 'ID Type', 'ID Path']
def check_customer_db():
    if not os.path.isfile(customer_db()):
        # Create a new customer.csv file with headers
        with open(customer_db(), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)
            log_message("Customer database created.")


class HyperlinkDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if index.column() == 7 and event.type() == QtCore.QEvent.MouseButtonRelease:
            text = index.data()
            if text:
                url = QtCore.QUrl.fromLocalFile(text)
                if QtGui.QDesktopServices.openUrl(url):
                    return True
        return super().editorEvent(event, model, option, index)
    
# OPEN DATABASE
def open_cust_database_viewer(self):
    width = 800  # Specify the desired width of the form
    height = 600  # Specify the desired height of the form
    self.database_window = DatabaseViewerForm(width, height, customer_db(),"Customer Database Viewer")
    self.database_window.show()
    log_message("Customer Database were viewed")

def open_serviceticket_database_viewer(self):
    width = 600  # Specify the desired width of the form
    height = 600  # Specify the desired height of the form
    self.database_window = DatabaseViewerForm(width, height, service_ticket_db(),"Service-Ticket Database Viewer")
    self.database_window.show()
    log_message("Service-Ticket Database were viewed")

class DatabaseViewerForm(QtWidgets.QMainWindow):
    def __init__(self, width, height, file_path, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setWindowIcon(QtGui.QIcon(tsystem_icon()))
        self.resize(width, height)
        self.table_widget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.load_csv_data(file_path)
        self.setup_table()
        self.search_results = []
        self.current_search_index = -1
        self.setup_search()

    def setup_table(self):
        delegate = HyperlinkDelegate(self.table_widget)
        self.table_widget.setItemDelegateForColumn(7, delegate)
        self.table_widget.verticalHeader().setVisible(False)

        blue_font_color = QtGui.QColor(QtCore.Qt.blue)
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 7)
            if item is not None:
                item.setForeground(blue_font_color)

    def setup_search(self):
        search_widget = QtWidgets.QWidget(self)
        search_widget.setMaximumWidth(300)
        search_layout = QtWidgets.QHBoxLayout(search_widget)
        search_label = QtWidgets.QLabel("Search:")
        search_line_edit = QtWidgets.QLineEdit()
        search_line_edit.setPlaceholderText("Enter search text")
        search_line_edit.setFixedWidth(300)
        search_line_edit.setFixedHeight(25)
        search_button = QtWidgets.QPushButton("Search")
        search_button.setFixedHeight(25)
        search_button.clicked.connect(lambda: self.search_data(search_line_edit.text()))
        next_button = QtWidgets.QPushButton("Next")
        next_button.setFixedHeight(25)
        next_button.clicked.connect(self.next_search_result)
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_line_edit)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(next_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(search_widget)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_widget)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_csv_data(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        num_rows = len(data)
        num_columns = len(data[0]) if data else 0
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns)

        for row in range(num_rows):
            for column in range(num_columns):
                item = QtWidgets.QTableWidgetItem(data[row][column])
                if column == 7:  # Column 8 (zero-based index)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_widget.setItem(row, column, item)

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_F:
            self.search_dialog()

    def search_dialog(self):
        search_dialog = QtWidgets.QDialog(self)
        search_dialog.setWindowTitle("Search")
        layout = QtWidgets.QVBoxLayout(search_dialog)
        search_label = QtWidgets.QLabel("Search:")
        search_line_edit = QtWidgets.QLineEdit()
        search_line_edit.setPlaceholderText("Enter search text")       
        search_button = QtWidgets.QPushButton("Search")
        search_button.clicked.connect(lambda: self.search_data(search_line_edit.text()))
        next_button = QtWidgets.QPushButton("Next")
        next_button.clicked.connect(self.next_search_result)
        self.next_button = next_button
        layout.addWidget(search_label)
        layout.addWidget(search_line_edit)
        layout.addWidget(search_button)
        layout.addWidget(next_button)
        search_dialog.exec_()

    def search_data(self, search_text):
        self.table_widget.clearSelection()
        self.search_results = self.table_widget.findItems(search_text, QtCore.Qt.MatchContains)
        self.current_search_index = -1
        self.next_search_result()

    def next_search_result(self):
        if self.search_results:
            if self.current_search_index == len(self.search_results) - 1:
                self.current_search_index = 0
            else:
                self.current_search_index += 1

            item = self.search_results[self.current_search_index]
            self.table_widget.setCurrentItem(item)
            self.table_widget.scrollToItem(item)
            self.table_widget.setFocus()

'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    width = 800  # Specify the desired width of the form
    height = 600  # Specify the desired height of the form
    database_window = DatabaseViewerForm(width, height, customer_db())
    log_message("Database was viewed")
    database_window.show()
    sys.exit(app.exec_())
'''
