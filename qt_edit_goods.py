from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Edit_goods(object):
    def setupUi(self, Edit_goods):
        Edit_goods.setObjectName("Edit_goods")
        Edit_goods.resize(700, 380)
        self.lineEdit_search = QtWidgets.QLineEdit(Edit_goods)
        self.lineEdit_search.setGeometry(QtCore.QRect(480, 20, 200, 30))
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.tableWidget_edit_goods = QtWidgets.QTableWidget(Edit_goods)
        self.tableWidget_edit_goods.setGeometry(QtCore.QRect(20, 60, 661, 251))
        self.tableWidget_edit_goods.setObjectName("tableWidget_edit_goods")
        self.layoutWidget = QtWidgets.QWidget(Edit_goods)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 310, 661, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_edit = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit.setObjectName("btn_edit")
        self.horizontalLayout.addWidget(self.btn_edit)
        self.btn_take_changes = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_take_changes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_take_changes.setObjectName("btn_take_changes")
        self.horizontalLayout.addWidget(self.btn_take_changes)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.btn_cancel_changes = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_cancel_changes.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cancel_changes.setObjectName("btn_cancel_changes")
        self.horizontalLayout.addWidget(self.btn_cancel_changes)

        self.retranslateUi(Edit_goods)
        QtCore.QMetaObject.connectSlotsByName(Edit_goods)

    def retranslateUi(self, Edit_goods):
        _translate = QtCore.QCoreApplication.translate
        Edit_goods.setWindowTitle(_translate("Edit_goods", "Редактирование товаров"))
        self.lineEdit_search.setPlaceholderText(_translate("Edit_goods", "Поиск..."))
        self.btn_edit.setText(_translate("Edit_goods", "Редактировать"))
        self.btn_take_changes.setText(_translate("Edit_goods", "Подтвердить изменения"))
        self.btn_delete.setText(_translate("Edit_goods", "Удалить"))
        self.btn_cancel_changes.setText(_translate("Edit_goods", "Отменить изменения"))
