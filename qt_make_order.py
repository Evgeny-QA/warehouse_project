from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_make_order(object):
    def setupUi(self, make_order):
        make_order.setObjectName("make_order")
        make_order.resize(700, 395)
        self.btn_cart = QtWidgets.QPushButton(make_order)
        self.btn_cart.setGeometry(QtCore.QRect(500, 350, 190, 30))
        self.btn_cart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart.setObjectName("btn_cart")
        self.btn_add_to_cart = QtWidgets.QPushButton(make_order)
        self.btn_add_to_cart.setGeometry(QtCore.QRect(20, 350, 190, 30))
        self.btn_add_to_cart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_to_cart.setObjectName("btn_add_to_cart")
        self.lineEdit_search_order = QtWidgets.QLineEdit(make_order)
        self.lineEdit_search_order.setGeometry(QtCore.QRect(490, 320, 200, 20))
        self.lineEdit_search_order.setFrame(False)
        self.lineEdit_search_order.setObjectName("lineEdit_search_order")
        self.lineEdit_quantity = QtWidgets.QLineEdit(make_order)
        self.lineEdit_quantity.setGeometry(QtCore.QRect(110, 320, 50, 20))
        self.lineEdit_quantity.setFrame(False)
        self.lineEdit_quantity.setPlaceholderText("")
        self.lineEdit_quantity.setObjectName("lineEdit_quantity")
        self.label_quantity = QtWidgets.QLabel(make_order)
        self.label_quantity.setGeometry(QtCore.QRect(20, 320, 70, 20))
        self.label_quantity.setObjectName("label_quantity")
        self.tableWidget_make_order = QtWidgets.QTableWidget(make_order)
        self.tableWidget_make_order.setGeometry(QtCore.QRect(10, 20, 680, 290))
        self.tableWidget_make_order.setObjectName("table_make_order")

        self.retranslateUi(make_order)
        QtCore.QMetaObject.connectSlotsByName(make_order)

    def retranslateUi(self, make_order):
        _translate = QtCore.QCoreApplication.translate
        make_order.setWindowTitle(_translate("make_order", "Оформление заказа"))
        self.btn_cart.setText(_translate("make_order", "Корзина"))
        self.btn_add_to_cart.setText(_translate("make_order", "Добавить в корзину"))
        self.lineEdit_search_order.setPlaceholderText(_translate("make_order", "Поиск..."))
        self.label_quantity.setText(_translate("make_order", "Колличество:"))
