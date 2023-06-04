import sys
import csv
import os
from PyQt5 import QtWidgets, QtGui, QtCore

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


class DatabaseViewerForm(QtWidgets.QMainWindow):
    def __init__(self, width, height, file_path):
        super().__init__()
        self.setWindowTitle("Customer Database Viewer")
        self.resize(width, height)
        self.table_widget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table_widget)
        self.load_csv_data(file_path)
        self.setup_table()

    def setup_table(self):
        delegate = HyperlinkDelegate(self.table_widget)
        self.table_widget.setItemDelegateForColumn(7, delegate)
        self.table_widget.verticalHeader().setVisible(False)

        blue_font_color = QtGui.QColor(QtCore.Qt.blue)
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 7)
            if item is not None:
                item.setForeground(blue_font_color)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    width = 800  # Specify the desired width of the form
    height = 600  # Specify the desired height of the form
    pwd_ = os.getcwd().replace('\\','/')  
    temp_db = pwd_+"/temp_db/"
    # customer database file path
    customer_db = temp_db+"customer.csv"
    database_window = DatabaseViewerForm(width, height, customer_db)
    database_window.show()
    sys.exit(app.exec_())
