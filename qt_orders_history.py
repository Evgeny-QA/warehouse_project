from PyQt5 import QtCore, QtGui, QtWidgets
from Db_functions import DataBase
from PyQt5.QtWidgets import QPushButton
from functools import partial
from os import startfile


def start_word_excel(path):
    return startfile(str(path))


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
        self.lineEdit.returnPressed.connect(self.fill_table())

    def fill_table(self):
        search = self.lineEdit.text()
        info = DataBase().get_completed_orders(search)
        self.tableWidget_table_history.setRowCount(len(info))
        for row, str_info in enumerate(info):
            len_str = len(str_info)
            for coll, info_insert in enumerate(str_info):
                if coll == len_str - 2:
                    button = QPushButton()
                    button.setText("Word")
                    button.clicked.connect(start_word_excel)
                    self.tableWidget_table_history.setCellWidget(row, coll, button)
                elif coll == len_str - 1:
                    button = QPushButton()
                    button.setText("Excel")
                    button.clicked.connect(start_word_excel)
                    self.tableWidget_table_history.setCellWidget(row, coll, button)
                else:
                    self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))
