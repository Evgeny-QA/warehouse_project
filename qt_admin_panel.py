import sqlite3
import traceback
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Admin_panel(object):
    def __init__(self):
        self.table = 'Users'
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()

    def setupUi(self, Admin_panel):
        Admin_panel.setObjectName("Admin_panel")
        Admin_panel.setWindowModality(QtCore.Qt.NonModal)
        Admin_panel.resize(660, 370)
        self.tableWidget = QtWidgets.QTableWidget(Admin_panel)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 620, 190))
        self.tableWidget.setObjectName("tableWidget")
        self.lineEdit_search = QtWidgets.QLineEdit(Admin_panel)
        self.lineEdit_search.setGeometry(QtCore.QRect(470, 10, 170, 30))
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.lineEdit_new_admin_data = QtWidgets.QLineEdit(Admin_panel)
        self.lineEdit_new_admin_data.setGeometry(QtCore.QRect(20, 260, 620, 25))
        self.lineEdit_new_admin_data.setFrame(False)
        self.lineEdit_new_admin_data.setObjectName("lineEdit_new_admin_data")
        self.layoutWidget = QtWidgets.QWidget(Admin_panel)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 310, 620, 40))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_edit = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit.setObjectName("btn_edit")
        self.horizontalLayout.addWidget(self.btn_edit)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.btn_add = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)

        self.show_data()

        self.retranslateUi(Admin_panel)
        QtCore.QMetaObject.connectSlotsByName(Admin_panel)

    def show_data(self):
        search_text = self.lineEdit_search.text()
        if search_text:
            self.cursor.execute("SELECT * FROM Users WHERE login LIKE ?", [f"%{search_text}%"])
        else:
            self.cursor.execute("SELECT * FROM Users")
        res = self.cursor.fetchall()
        if not res:
            QtWidgets.QMessageBox.information(self.tableWidget, 'Поиск', 'Данные не найдены!')
        else:
            column_names = [column[0] for column in self.cursor.description]
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(len(res[0]))
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            for row_number, row_data in enumerate(res):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.lineEdit_search.clear()

    def retranslateUi(self, Admin_panel):
        _translate = QtCore.QCoreApplication.translate
        Admin_panel.setWindowTitle(_translate("Admin_panel", "Панель администратора"))
        self.lineEdit_search.setPlaceholderText(_translate("Admin_panel", "Поиск..."))
        self.lineEdit_new_admin_data.setPlaceholderText(_translate("Admin_panel", "Введите Имя и Пароль нового пользователя"))
        self.btn_edit.setText(_translate("Admin_panel", "Редактировать"))
        self.btn_delete.setText(_translate("Admin_panel", "Удалить"))
        self.btn_add.setText(_translate("Admin_panel", "Добавить"))
        self.btn_add.clicked.connect(partial(self.add_new_admin))
        self.btn_delete.clicked.connect(partial(self.delete_admin))
        self.btn_edit.clicked.connect(partial(self.change_data))
        self.lineEdit_search.returnPressed.connect(partial(self.show_data))

    def add_new_admin(self):
        if len(self.lineEdit_new_admin_data.text().split(',')) != 2:
            return QtWidgets.QMessageBox.information(self.tableWidget, 'Добавление администратора',
                                              'Введены некорректные данные!\nВведите данные в формате Имя, Пароль.')

        self.login = self.lineEdit_new_admin_data.text().split(',')[0].strip()
        self.password = self.lineEdit_new_admin_data.text().split(',')[1].strip()

        self.cursor.execute(f"INSERT INTO Users(login, password) VALUES(?,?)", [self.login, self.password])
        self.db.commit()
        self.lineEdit_new_admin_data.clear()
        self.show_data()

    def delete_admin(self):
        try:
            selected_rows = self.tableWidget.selectedItems()
            if not selected_rows:
                return

            selected_ids = set(item.data(QtCore.Qt.DisplayRole) for item in selected_rows if item.column() == 0)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Удаление пользователя')
            msg.setText("Вы уверены, что хотите удалить пользователя(лей)?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            btn = msg.exec_()
            if btn == QtWidgets.QMessageBox.Ok:
                for selected_id in selected_ids:
                    self.cursor.execute(f"DELETE FROM Users WHERE id = ?", [selected_id])
            self.db.commit()
            self.show_data()

        except Exception as e:
            traceback.print_exc()

    def change_data(self):
        selected_fields = self.tableWidget.selectedItems()
        if not selected_fields:
            return

        for field in selected_fields:
            row = field.row()
            column = field.column()
            new_value = field.text()
            user_id = self.tableWidget.item(row, 0).text()

            self.cursor.execute(
                f"UPDATE Users SET {self.tableWidget.horizontalHeaderItem(column).text()} = ? WHERE id = ?",
                [new_value, user_id])

        self.db.commit()
        self.show_data()


