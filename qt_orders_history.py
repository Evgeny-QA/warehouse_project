from PyQt5 import QtCore, QtGui, QtWidgets
from Db_functions import DataBase
from PyQt5.QtWidgets import QPushButton
from os import startfile


class Ui_Orders_History(object):
    def __init__(self, user):
        self.current_user = user

    def setupUi(self, Orders_History):
        Orders_History.setObjectName("Orders_History")
        Orders_History.resize(600, 320)
        self.tableWidget_table_history = QtWidgets.QTableWidget(Orders_History)
        self.tableWidget_table_history.setGeometry(QtCore.QRect(20, 60, 560, 240))
        self.tableWidget_table_history.setObjectName("tableWidget_table_history")
        self.lineEdit = QtWidgets.QLineEdit(Orders_History)
        self.lineEdit.setGeometry(QtCore.QRect(370, 20, 200, 30))
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Orders_History)
        QtCore.QMetaObject.connectSlotsByName(Orders_History)

        table_collums = ["№ Заказа", "Составитель ТТН", "Компания (заказчик)", "Адрес доставки", "Word", "Excel"]
        self.tableWidget_table_history.setColumnCount(len(table_collums))
        self.tableWidget_table_history.setHorizontalHeaderLabels(table_collums)
        self.fill_table()

    def retranslateUi(self, Orders_History):
        _translate = QtCore.QCoreApplication.translate
        Orders_History.setWindowTitle(_translate("Orders_History", "История заказов"))
        self.lineEdit.setPlaceholderText(_translate("Orders_History", "Поиск..."))
        self.lineEdit.returnPressed.connect(self.fill_table)

    def start_word_excel(self, path):
        return startfile(path)

    def input_file_button(self, row, coll, file_text, file_path):
        button = QPushButton()
        button.setText(file_text)
        button.clicked.connect(lambda: self.start_word_excel(file_path))
        #button.clicked.connect(start_word_excel(file_path))    doesn't work
        self.tableWidget_table_history.setCellWidget(row, coll, button)

    def fill_table(self):
        search_text = self.lineEdit.text()
        print([search_text])
        info = DataBase().get_completed_orders(search_text)
        if len(info) == 0:
            QtWidgets.QMessageBox.information(self.tableWidget_table_history, 'Ошибка поиска', 'Данные не найдены!')
            return
        self.tableWidget_table_history.setRowCount(len(info))
        for row, str_info in enumerate(info):
            len_str = len(str_info)
            for coll, info_insert in enumerate(str_info):
                if coll == len_str - 2:
                    self.input_file_button(row, coll, "Word", info_insert)
                elif coll == len_str - 1:
                    self.input_file_button(row, coll, "Excel", info_insert)
                else:
                    self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))
