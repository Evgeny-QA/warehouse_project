from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3


class Ui_Orders_History(object):
    def __init__(self, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.current_user = user

    def setupUi(self, Orders_History):
        Orders_History.setObjectName("Orders_History")
        Orders_History.resize(600, 320)
        self.btn_open_documcent = QtWidgets.QPushButton(Orders_History)
        self.btn_open_documcent.setGeometry(QtCore.QRect(20, 260, 190, 30))
        self.btn_open_documcent.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_open_documcent.setObjectName("btn_open_documcent")
        self.tableWidget_table_history = QtWidgets.QTableWidget(Orders_History)
        self.tableWidget_table_history.setGeometry(QtCore.QRect(20, 20, 560, 220))
        self.tableWidget_table_history.setObjectName("tableWidget_table_history")
        self.lineEdit = QtWidgets.QLineEdit(Orders_History)
        self.lineEdit.setGeometry(QtCore.QRect(370, 260, 200, 30))
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Orders_History)
        QtCore.QMetaObject.connectSlotsByName(Orders_History)

    def retranslateUi(self, Orders_History):
        _translate = QtCore.QCoreApplication.translate
        Orders_History.setWindowTitle(_translate("Orders_History", "История заказов"))
        self.btn_open_documcent.setText(_translate("Orders_History", "Открыть документ"))
        self.lineEdit.setPlaceholderText(_translate("Orders_History", "Поиск..."))
