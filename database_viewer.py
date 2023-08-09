# Anthony's Home Appliance Repair Ticketing System
# Common packages and customize scripts
from backend.public_backend import *

# Customize scripts
from backend.logs_generator import *

# Task bar icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
     
class HyperlinkDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def editorEvent(self, event, model, option, index):
        if index.column() == 7 and event.type() == QEvent.MouseButtonRelease:
            # Adding id_db() so the id can be view even if there's any changes in the directory
            text = id_db_dir + index.data()
            if text:
                url = QUrl.fromLocalFile(text)
                if QDesktopServices.openUrl(url):
                    return True
        return super().editorEvent(event, model, option, index)
      
# OPEN DATABASE
def open_cust_database_viewer(self):
    try:
        width = 850  # Specify the desired width of the form
        height = 600  # Specify the desired height of the form
        self.database_window = DatabaseViewerForm(width, height, customer_db_dir, "Customer Database Viewer")
        #self.database_window.setGeometry(self.geometry().x() - width, self.geometry().y(), width, height)
        self.database_window.show()
        log_message("Customer Database was viewed")
    except Exception as e:
        # Log the exception message and traceback
        QMessageBox.information(None, "AHARTS", default_err_msg)
        error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
        log_message(error_message)

def open_serviceticket_database_viewer(self):
    try:
        width = 700  # Specify the desired width of the form
        height = 600  # Specify the desired height of the form
        self.database_window = DatabaseViewerForm(width, height, service_ticket_db_dir, "Service-Ticket Database Viewer")
        #self.database_window.setGeometry(self.geometry().x() + self.width(), self.geometry().y(), width, height)
        self.database_window.show()
        log_message("Service-Ticket Database was viewed")
    except Exception as e:
        # Log the exception message and traceback
        QMessageBox.information(None, "AHARTS", default_err_msg)
        error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
        log_message(error_message)

def open_ts_order_database_viewer(self):
    try:
        width = 700  # Specify the desired width of the form
        height = 600  # Specify the desired height of the form
        self.database_window = DatabaseViewerForm(width, height, troubleshooting_order_db_dir, "Troubleshooting Order Database Viewer")
        #self.database_window.setGeometry(self.geometry().x() + self.width(), self.geometry().y(), width, height)
        self.database_window.show()
        log_message("Troubleshooting Order Database was viewed")
    except Exception as e:
        # Log the exception message and traceback
        QMessageBox.information(None, "AHARTS", default_err_msg)
        error_message = f"Error: {e}\nTraceback: {traceback.format_exc()}"
        log_message(error_message)


class DatabaseViewerForm(QMainWindow):
    def __init__(self, width, height, file_path, window_title):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon(tsystem_icon))
        self.resize(width, height)
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.load_parquet_data(file_path)
        self.setup_table()
        self.search_results = []
        self.current_search_index = -1
        self.setup_search()

        self.db_table = file_path

    def setup_table(self):
        delegate = HyperlinkDelegate(self.table_widget)
        self.table_widget.setItemDelegateForColumn(7, delegate)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setItemDelegate(delegate)

        blue_font_color = QColor(Qt.blue)
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 7)
            if item is not None:
                item.setForeground(blue_font_color)

    def setup_search(self):
        search_widget = QWidget(self)
        search_widget.setMaximumWidth(300)
        search_layout = QHBoxLayout(search_widget)
        search_label = QLabel("Search:")
        search_line_edit = QLineEdit()
        search_line_edit.setPlaceholderText("Enter search text")
        search_line_edit.setFixedWidth(300)
        search_line_edit.setFixedHeight(25)
        search_button = QPushButton("Search")
        search_button.setFixedHeight(25)
        search_button.clicked.connect(lambda: self.search_data(search_line_edit.text()))
        next_button = QPushButton("Next")
        next_button.setFixedHeight(25)
        next_button.clicked.connect(self.next_search_result)
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_line_edit)
        import_button = QPushButton("Import Data")
        export_button = QPushButton("Export Data")
        import_button.clicked.connect(lambda: import_to_parquet(self, self.db_table))
        export_button.clicked.connect(lambda: export_to_csv(self, self.db_table))

        button_layout = QHBoxLayout()
        button_layout.addWidget(search_button)
        button_layout.addWidget(next_button)
        button_layout.addWidget(import_button)
        button_layout.addWidget(export_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widget)      
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_parquet_data(self, file_path):
        df = pd.read_parquet(file_path)
        column_headers = df.columns.tolist()
        num_rows, num_columns = df.shape
        self.table_widget.setRowCount(num_rows)
        self.table_widget.setColumnCount(num_columns)

        # Set column headers
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        for row in range(num_rows):
            for column in range(num_columns):
                item = QTableWidgetItem(str(df.iloc[row, column]))
                if column == 7:  # Column 8 (zero-based index)
                    item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(row, column, item)


    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            self.search_dialog()

    def search_dialog(self):
        search_dialog = QDialog(self)
        search_dialog.setWindowTitle("Search")
        layout = QVBoxLayout(search_dialog)
        search_label = QLabel("Search:")
        search_line_edit = QLineEdit()
        search_line_edit.setPlaceholderText("Enter search text")       
        search_button = QPushButton("Search")
        search_button.clicked.connect(lambda: self.search_data(search_line_edit.text()))
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_search_result)
        self.next_button = next_button
        layout.addWidget(search_label)
        layout.addWidget(search_line_edit)
        layout.addWidget(search_button)
        layout.addWidget(next_button)
        search_dialog.exec_()

    def search_data(self, search_text):
        self.table_widget.clearSelection()
        self.search_results = self.table_widget.findItems(search_text, Qt.MatchContains)
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

# Export parquet data to csv
def export_to_csv(self,db_table):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)
    dialog.setOption(QFileDialog.ShowDirsOnly)
    dialog.setOption(QFileDialog.DontUseNativeDialog)
    folder_path = dialog.getExistingDirectory(self, "Select Folder")
        
    if folder_path:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Proceed to export the data to CSV?")
        msgBox.setWindowTitle("AHARTS")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msgBox.buttonClicked.connect(QMessageBox)

        # Generate the new filename with the current date
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Generate timestamping for each log
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Replace colons in the filename with periods
        current_time = current_time.replace(":", ".")

        filename = self.windowTitle().replace(" ", "_")

        csv_file = f'{folder_path}/{filename}_{current_date}_{current_time}.csv'

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            # Read the Parquet file into a DataFrame
            df = pd.read_parquet(db_table)
                
            # Convert DataFrame to CSV file
            df.to_csv(csv_file, index=False)

            # Log the export message
            message = f"Customer Database has been exported to:\n{csv_file}"
            QMessageBox.information(None, "AHARTS", message)
            log_message(message)


def import_to_parquet(self, db_table):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.ExistingFile)
    dialog.setNameFilter("CSV Files (*.csv)")
    dialog.setOption(QFileDialog.DontUseNativeDialog)
    csv_file, _ = dialog.getOpenFileName(self, "Select CSV File")

    if csv_file:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Are you sure you want to import these data to database?")
        msgBox.setWindowTitle("AHARTS")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msgBox.buttonClicked.connect(QMessageBox)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            df_csv = pd.read_csv(csv_file)

            # Read the existing Parquet file
            df_parquet = pd.read_parquet(db_table)

            # Append the CSV data to the Parquet file
            df_combined = pd.concat([df_parquet, df_csv], ignore_index=True)

            # Save the combined data to a new Parquet file
            df_combined.to_parquet(db_table, index=False)

            # Update display in database viewer
            self.load_parquet_data(db_table)

            message = "CSV data has been imported and appended to the Parquet file."
            QMessageBox.information(None, "AHARTS", message)
            log_message(message)


'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    width = 800  # Specify the desired width of the form
    height = 600  # Specify the desired height of the form
    database_window = DatabaseViewerForm(width, height, customer_db())
    log_message("Database was viewed")
    database_window.show()
    sys.exit(app.exec_())
'''
