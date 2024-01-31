from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import sqlite3


class Ui_Client_data(object):
    def __init__(self, cart_class, user, goods_in_cart, all_price):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.cart_class = cart_class
        self.current_user = user
        self.goods_in_order = goods_in_cart
        self.price = all_price
        self.data = None
        self.address = None

    def setupUi(self, Client_data):
        Client_data.setObjectName("Client_data_and_address")
        Client_data.resize(400, 250)
        self.lineEdit_client = QtWidgets.QLineEdit(Client_data)
        self.lineEdit_client.setGeometry(QtCore.QRect(20, 50, 360, 30))
        self.lineEdit_client.setFrame(False)
        self.lineEdit_client.setObjectName("lineEdit_client")
        self.lineEdit_address = QtWidgets.QLineEdit(Client_data)
        self.lineEdit_address.setGeometry(QtCore.QRect(20, 140, 360, 30))
        self.lineEdit_address.setFrame(False)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.layoutWidget = QtWidgets.QWidget(Client_data)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 190, 280, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_take_data = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_take_data.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_take_data.setObjectName("btn_take_data")
        self.horizontalLayout.addWidget(self.btn_take_data)
        self.btn_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.comboBox_client = QtWidgets.QComboBox(Client_data)
        self.comboBox_client.setGeometry(QtCore.QRect(20, 20, 360, 20))
        self.comboBox_client.setObjectName("comboBox_client")
        self.comboBox_address = QtWidgets.QComboBox(Client_data)
        self.comboBox_address.setGeometry(QtCore.QRect(20, 110, 360, 20))
        self.comboBox_address.setObjectName("comboBox_address")

        self.comboBox_client.currentIndexChanged.connect(self.combo_box_client)
        self.comboBox_address.currentIndexChanged.connect(self.combo_box_address)
        self.get_companies_list()
        Client_data.closeEvent = self.close_window

        self.retranslateUi(Client_data)
        QtCore.QMetaObject.connectSlotsByName(Client_data)

    def retranslateUi(self, Client_data):
        _translate = QtCore.QCoreApplication.translate
        Client_data.setWindowTitle(_translate("Client_data_and_address", "Данные клиента"))
        self.lineEdit_client.setPlaceholderText(_translate("Client_data_and_address", "Введите данные заказчика"))
        self.lineEdit_address.setPlaceholderText(_translate("Client_data", "Введите адрес доставки (Город, улица, дом, почтовый индекс)"))
        self.btn_take_data.setText(_translate("Client_data_and_address", "Принять"))
        self.btn_cancel.setText(_translate("Client_data_and_address", "Отмена"))
        self.btn_take_data.clicked.connect(partial(self.get_data))

    def get_data(self):
        if len(self.lineEdit_client.text()) > 0:
            self.data = self.lineEdit_client.text()
        else:
            return QtWidgets.QMessageBox.information(self.layoutWidget, 'Ошибка', 'Введите данные клиента!')
        if len(self.lineEdit_address.text()) > 0:
            self.address = self.lineEdit_address.text()
        else:
            return QtWidgets.QMessageBox.information(self.layoutWidget, 'Ошибка', 'Введите адрес!')

    def get_companies_list(self):
        self.comboBox_client.clear()
        companies = ["Вписать данные самостоятельно"]
        self.cursor.execute("SELECT * FROM Companies")
        companies_db = self.cursor.fetchall()
        companies += [i[1] for i in companies_db]
        for company in companies:
            self.comboBox_client.addItem(company)

        addresses = ["Вписать адрес самостоятельно"]
        addresses += [i[2] for i in companies_db]
        for address in addresses:
            self.comboBox_address.addItem(address)

    def combo_box_client(self, index_client):
        if index_client == 0:
            self.lineEdit_client.clear()
            self.lineEdit_client.setEnabled(True)
        else:
            selected_company = self.comboBox_client.currentText()
            self.lineEdit_client.setText(selected_company)
            self.lineEdit_client.setEnabled(False)

    def combo_box_address(self, index_address):
        if index_address == 0:
            self.lineEdit_address.clear()
            self.lineEdit_address.setEnabled(True)
        else:
            selected_address = self.comboBox_address.currentText()
            self.lineEdit_address.setText(selected_address)
            self.lineEdit_address.setEnabled(False)

    def close_window(self, event):
        self.cart_class.current_window.show()
        event.accept()
