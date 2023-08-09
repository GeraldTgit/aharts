from backend.public_backend import *
from backend.connect_to_aws import *

import threading

def open_settings(self):
    self.database_window = SettingsWindow(self)
    self.database_window.show()

class SettingsWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(tsystem_icon))

        # Store a reference to the main form
        self.main_window = main_window
        
        # Create a main widget and set it as the central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a layout for the main widget
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignCenter)

        header_label = QLabel("Settings")
        header_label.setFont(QFont('Arial', 20))
        layout.addWidget(header_label, alignment=Qt.AlignCenter)

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

        header_label_1 = QLabel("AWS S3 Bucket")
        header_label_1.setFont(QFont('Arial', 12))
        layout.addWidget(header_label_1)

        aws_button = QPushButton("Check For Connection", clicked = lambda: self.check_aws_connection())
        layout.addWidget(aws_button)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        self.log_label = QLabel('')
        layout.addWidget(self.log_label)

        # Broken Line
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1, styleSheet=dash_line_style))

        # Draw a horizontal line -----------------------------------------------------------------------------
        layout.addWidget(QFrame(self, frameShape=QFrame.HLine, frameShadow=QFrame.Sunken, lineWidth=1))

    def check_aws_connection(self):
        self.log_label.setText(f"{process_dttm()} Connecting...")

        # Create threads for each AWS operation
        thread_objects = threading.Thread(target=self.check_objects_in_bucket)
        thread_databases = threading.Thread(target=self.check_databases)

        # Start the threads
        thread_objects.start()
        thread_databases.start()


    def check_objects_in_bucket(self):
        logs = check_objects_in_bucket()  # Call the function without self.
        self.update_label(logs)

    def check_databases(self):
        logs = check_databases()  # Call the function without self.
        self.update_label(logs)

    def term_conx(self): # Terminate connection
        self.update_label(['---',f'{process_dttm()} Connection terminated'])

    def update_label(self, logs):
        # Update the label with the received logs
        current_text = self.log_label.text()
        join_logs = '\n'.join(logs)
        new_text = f"{current_text}\n{join_logs}"
        self.log_label.setText(new_text)
