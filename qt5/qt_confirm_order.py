from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(290, 200)
        self.lineEdit_client_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_client_2.setGeometry(QtCore.QRect(20, 30, 250, 30))
        self.lineEdit_client_2.setFrame(False)
        self.lineEdit_client_2.setObjectName("lineEdit_client_2")
        self.lineEdit_adress = QtWidgets.QLineEdit(Form)
        self.lineEdit_adress.setGeometry(QtCore.QRect(20, 80, 250, 30))
        self.lineEdit_adress.setFrame(False)
        self.lineEdit_adress.setObjectName("lineEdit_adress")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 130, 251, 31))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_ok = QtWidgets.QPushButton(self.widget)
        self.btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.btn_cancel = QtWidgets.QPushButton(self.widget)
        self.btn_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit_client_2.setPlaceholderText(_translate("Form", "Введите данные заказчика..."))
        self.lineEdit_adress.setPlaceholderText(_translate("Form", "Введите адрес доставки..."))
        self.btn_ok.setText(_translate("Form", "Подтвердить"))
        self.btn_cancel.setText(_translate("Form", "Отмена"))
