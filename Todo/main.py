from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from DatabaseHandler import DatabaseHandler

class Ui_MainWindow(object):
    def __init__(self):
        self.database_handler = DatabaseHandler()  # Burada self.database_handler tanımlanmalı
        self.selected_record_id = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1061, 853)
        MainWindow.setStyleSheet("QMainWindow{\n"
        "    background-color:rgb(255, 210, 211)\n"
        "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(230, 0, 591, 211))
        self.widget.setStyleSheet("QWidget{\n"
        "    background-color:white\n"
        "}")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 101, 31))
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.titleEdit = QtWidgets.QLineEdit(self.widget)
        self.titleEdit.setGeometry(QtCore.QRect(110, 10, 281, 31))
        self.titleEdit.setText("")
        self.titleEdit.setObjectName("titleEdit")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 10, 51, 31))
        self.label.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.contentEdit = QtWidgets.QLineEdit(self.widget)
        self.contentEdit.setGeometry(QtCore.QRect(110, 50, 281, 141))
        self.contentEdit.setText("")
        self.contentEdit.setObjectName("contentEdit")
        self.updateButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.update_func())
        self.updateButton.setGeometry(QtCore.QRect(670, 80, 131, 41))
        self.updateButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    background-color:yellow\n"
        "}")
        self.updateButton.setObjectName("updateButton")
        self.addButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.add_func())
        self.addButton.setGeometry(QtCore.QRect(670, 10, 131, 41))
        self.addButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    background-color:green\n"
        "}")
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.delete_func())
        self.deleteButton.setGeometry(QtCore.QRect(670, 150, 131, 41))
        self.deleteButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    background-color:red\n"
        "}")
        self.deleteButton.setObjectName("updateButton")
        self.filterButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.filter_func())
        self.filterButton.setGeometry(QtCore.QRect(530, 230, 131, 41))
        self.filterButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    background-color:blue\n"
        "}")
        self.filterButton.setObjectName("refreshButton")

        self.refreshButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.refresh_func())
        self.refreshButton.setGeometry(QtCore.QRect(750, 230, 150, 41))
        self.refreshButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    background-color:orange\n"
        "}")
        self.refreshButton.setObjectName("refreshButton")
        
        # QTableWidget tanımlaması
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(230, 300, 831, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Id", "Title", "Status", "Open Date", "Days Open", "Content"])

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(230, 230, 281, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(-1, -1, 221, 781))
        self.widget_2.setStyleSheet("QWidget{\n"
        "background-color:rgb(64, 106, 107)\n"
        "}")
        self.widget_2.setObjectName("widget_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1061, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Reload the table
        self.load_table()
        self.tableWidget.selectionModel().selectionChanged.connect(self.on_table_selection_change)
 
    def refresh_func(self):
        self.load_table()

    def filter_func(self):
        filtered_data = self.comboBox.currentText()
    
        #gets filtered datas
        filtered_results = self.database_handler.filter_datas(filtered_data)
    
        #clear table
        self.tableWidget.setRowCount(0)
    
        #Adding filtered datas to table
        for row_data in filtered_results:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
        
                for column, item in enumerate(row_data):
                        self.tableWidget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(item)))

    def update_days_open(self):
        #Gets datas from Database
        data = self.database_handler.fetch_all_data()

        #(current_date2)
        current_date2 = datetime.now()
        formatted_date2 = current_date2.strftime("%d/%m/%Y")
        date2 = datetime.strptime(formatted_date2, "%d/%m/%Y")

        #Loop
        for row in data:
            record_id = row[0]
            open_date_str = row[1]
            open_date = datetime.strptime(open_date_str, "%d/%m/%Y")
            

            difference = date2 - open_date
            days_open = difference.days


            self.database_handler.update_days_open(record_id, days_open)

        self.load_table()


    def load_table(self):
        #Gets datas from db and fill the table
        data = self.database_handler.fetch_all_data()
        # Clear old datas
        self.tableWidget.setRowCount(0)  

        for row in data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, item in enumerate(row):
                self.tableWidget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(item)))
         
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Content:"))
        self.label.setText(_translate("MainWindow", "Title:"))
        self.updateButton.setText(_translate("MainWindow", "Update Todo"))
        self.addButton.setText(_translate("MainWindow", "Add Todo"))
        self.deleteButton.setText(_translate("MainWindow", "Delete Todo"))
        self.filterButton.setText(_translate("MainWindow", "Filter"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Title"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Open Date"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Days Open"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Content"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Open"))
        self.comboBox.setItemText(1, _translate("MainWindow", "In Progress"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Done"))


    def add_func(self):
        titleText = self.titleEdit.text()
        statusText = self.comboBox.currentText()

        #First Date
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d/%m/%Y")

        #Second Date
        current_date2 = datetime.now()
        formatted_date2 = current_date2.strftime("%d/%m/%Y")

        #Formatting
        date1 = datetime.strptime(formatted_date, "%d/%m/%Y")
        date2 = datetime.strptime(formatted_date2, "%d/%m/%Y")

        #Difference
        difference = date2 - date1
        daysOpen = difference.days

        contentText = self.contentEdit.text()

        self.database_handler.add_data(titleText, statusText, formatted_date, daysOpen, contentText)
        #Clear the textBoxes and comboBox
        self.titleEdit.setText("")
        self.contentEdit.setText("")
        self.comboBox.setCurrentIndex(0)
        self.load_table()

    def on_table_selection_change(self):
                #When selected a row
                selected_row = self.tableWidget.currentRow()
                if selected_row >= 0:
                        self.selected_record_id = self.tableWidget.item(selected_row, 0).text()
                        title = self.tableWidget.item(selected_row, 1).text()
                        status = self.tableWidget.item(selected_row, 2).text()
                        content = self.tableWidget.item(selected_row, 5).text()

                        #Send datas to UI components
                        self.titleEdit.setText(title)
                        self.contentEdit.setText(content)
                        self.comboBox.setCurrentText(status)    

    def update_func(self):
        #Update the database and refresh the table
        if self.selected_record_id is not None:
            #get new datas from user
            titleText = self.titleEdit.text()
            statusText = self.comboBox.currentText()
            contentText = self.contentEdit.text()
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d/%m/%Y")
            daysOpen = 0 

            #Update in database
            self.database_handler.update_data(self.selected_record_id, titleText, statusText, formatted_date, daysOpen, contentText)

            #Refresh teh table
            self.load_table()

            #Clear the textBoxes and comboBox
            self.titleEdit.setText("")
            self.contentEdit.setText("")
            self.comboBox.setCurrentIndex(0)

    def delete_func(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
                #Gets ID of selected row
                item_id = self.tableWidget.item(selected_row, 0).text()

                #Delete from todo.db database
                self.database_handler.delete_data(item_id)

                #Reload the table
                self.load_table()

    def fetch_all_data(self):
        return self.database_handler.fetch_all_data()
    
    def load_table(self):
        data = self.fetch_all_data()
    
        self.tableWidget.setRowCount(0)

        for row in data:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for column, item in enumerate(row):
                        self.tableWidget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(item)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
