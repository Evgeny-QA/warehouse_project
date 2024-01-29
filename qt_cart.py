from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Cart(object):
    def setupUi(self, Cart):
        Cart.setObjectName("Cart")
        Cart.resize(490, 380)
        self.tableWidget = QtWidgets.QTableWidget(Cart)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 450, 280))
        self.tableWidget.setObjectName("tableWidget")
        self.layoutWidget = QtWidgets.QWidget(Cart)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 330, 450, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_cart_get_order = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_get_order.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_get_order.setObjectName("btn_cart_get_order")
        self.horizontalLayout.addWidget(self.btn_cart_get_order)
        self.btn_cart_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_delete.setObjectName("btn_cart_delete")
        self.horizontalLayout.addWidget(self.btn_cart_delete)
        self.btn_cart_clear = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cart_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart_clear.setObjectName("btn_cart_clear")
        self.horizontalLayout.addWidget(self.btn_cart_clear)

        self.retranslateUi(Cart)
        QtCore.QMetaObject.connectSlotsByName(Cart)

    def retranslateUi(self, Cart):
        _translate = QtCore.QCoreApplication.translate
        Cart.setWindowTitle(_translate("Cart", "Корзина"))
        self.btn_cart_get_order.setText(_translate("Cart", "Подтвердить заказ"))
        self.btn_cart_delete.setText(_translate("Cart", "Удалить"))
        self.btn_cart_clear.setText(_translate("Cart", "Очистить корзину"))
