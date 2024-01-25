from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_add_good(object):
    def setupUi(self, add_good):
        add_good.setObjectName("add_good")
        add_good.resize(600, 300)
        self.table_add_good = QtWidgets.QTableView(add_good)
        self.table_add_good.setGeometry(QtCore.QRect(20, 30, 560, 180))
        self.table_add_good.setObjectName("table_add_good")
        self.layoutWidget = QtWidgets.QWidget(add_good)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 240, 500, 25))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_add_good = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_add_good.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_good.setObjectName("btn_add_good")
        self.horizontalLayout.addWidget(self.btn_add_good)
        self.btn_clear_data = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_clear_data.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_clear_data.setObjectName("btn_clear_data")
        self.horizontalLayout.addWidget(self.btn_clear_data)

        self.retranslateUi(add_good)
        QtCore.QMetaObject.connectSlotsByName(add_good)

    def retranslateUi(self, add_good):
        _translate = QtCore.QCoreApplication.translate
        add_good.setWindowTitle(_translate("add_good", "Добавление товара"))
        self.btn_add_good.setText(_translate("add_good", "Добавить товар"))
        self.btn_clear_data.setText(_translate("add_good", "Очистить данные"))
