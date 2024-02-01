import sqlite3
import traceback
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Admin_panel(object):
    def __init__(self, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.current_user = user
        self.info_for_search = None

    def setupUi(self, Admin_panel):
        Admin_panel.setObjectName("Admin_panel")
        Admin_panel.setWindowModality(QtCore.Qt.NonModal)
        Admin_panel.resize(375, 335)
        self.tableWidget = QtWidgets.QTableWidget(Admin_panel)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 335, 190))
        self.tableWidget.setObjectName("tableView_data")
        self.lineEdit_search = QtWidgets.QLineEdit(Admin_panel)
        self.lineEdit_search.setGeometry(QtCore.QRect(180, 10, 170, 25))
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.lineEdit_new_admin_login = QtWidgets.QLineEdit(Admin_panel)
        self.lineEdit_new_admin_login.setGeometry(QtCore.QRect(20, 260, 150, 20))
        self.lineEdit_new_admin_login.setFrame(False)
        self.lineEdit_new_admin_login.setObjectName("lineEdit_new_admin_login")
        self.lineEdit_new_admin_password = QtWidgets.QLineEdit(Admin_panel)
        self.lineEdit_new_admin_password.setGeometry(QtCore.QRect(200, 260, 150, 18))
        self.lineEdit_new_admin_password.setFrame(False)
        self.lineEdit_new_admin_password.setObjectName("lineEdit_new_admin_password")
        self.btn_edit = QtWidgets.QPushButton(Admin_panel)
        self.btn_edit.setGeometry(QtCore.QRect(20, 10, 90, 25))
        self.btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit.setObjectName("btn_edit")
        self.widget = QtWidgets.QWidget(Admin_panel)
        self.widget.setGeometry(QtCore.QRect(20, 290, 330, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_delete = QtWidgets.QPushButton(self.widget)
        self.btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.btn_add = QtWidgets.QPushButton(self.widget)
        self.btn_add.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)

        self.get_info_from_db()
        self.show_data()

        self.retranslateUi(Admin_panel)
        QtCore.QMetaObject.connectSlotsByName(Admin_panel)

    def retranslateUi(self, Admin_panel):
        _translate = QtCore.QCoreApplication.translate
        Admin_panel.setWindowTitle(_translate("Admin_panel", "Панель администратора"))
        self.lineEdit_search.setPlaceholderText(_translate("Admin_panel", "Поиск..."))
        self.lineEdit_new_admin_login.setPlaceholderText(_translate("Admin_panel", "Введите Login"))
        self.btn_edit.setText(_translate("Admin_panel", "Редактировать"))
        self.btn_delete.setText(_translate("Admin_panel", "Удалить"))
        self.btn_add.setText(_translate("Admin_panel", "Добавить"))
        self.lineEdit_new_admin_password.setPlaceholderText(_translate("Admin_panel", "Введите Пароль"))
        self.btn_add.clicked.connect(partial(self.add_new_admin))
        self.btn_delete.clicked.connect(partial(self.delete_admin))
        self.btn_edit.clicked.connect(partial(self.change_data))
        self.lineEdit_search.returnPressed.connect(partial(self.show_data))

    def get_info_from_db(self):
        self.cursor.execute(f"SELECT * FROM Users")
        self.info_for_search = self.cursor.fetchall()

    def show_data(self):
        search_text = self.lineEdit_search.text()
        if search_text:
            res = []
            for info in self.info_for_search:
                if info[1].lower() == search_text or info[1].lower().startswith(search_text.lower()):
                    res.append(info)
            self.fill_table(res) if res != [] else (
                QtWidgets.QMessageBox.information(self.tableWidget, 'Ошибка поиска', 'Данные не найдены!'))
        else:
            return self.fill_table(self.info_for_search) if self.info_for_search !=[] else(
                QtWidgets.QMessageBox.information(self.tableWidget, 'Ошибка поиска', 'Данные не найдены!'))

    def fill_table(self, info):
        column_names = ['ID', 'Имя(login)', 'Пароль']
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(info[0]))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for row_number, row_data in enumerate(info):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                if column_number == 0:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_number, column_number, item)

    def add_new_admin(self):
        login = self.lineEdit_new_admin_login.text().strip()
        password = self.lineEdit_new_admin_password.text().strip()

        if not login:
            return QtWidgets.QMessageBox.information(self.tableWidget, 'Ошибка!', 'Введите Login (Имя пользователя).')
        if not password:
            return QtWidgets.QMessageBox.information(self.tableWidget, 'Ошибка!', 'Введите password (Пароль).')
        self.cursor.execute("SELECT login FROM Users WHERE login = ?", [login])
        login_check = self.cursor.fetchone()
        if login_check is not None:
            return QtWidgets.QMessageBox.information(self.tableWidget,
                            'Ошибка!', f'Пользователь "{login}" уже зарегистрирован.\nВведите другой login.')
        else:
            self.cursor.execute(f"INSERT INTO Users(login, password) VALUES(?,?)", [login, password])
            self.db.commit()
            QtWidgets.QMessageBox.information(self.tableWidget, 'Информация!',
                                              f'Пользователь {login} упсешно зарегистрирован.')
        self.lineEdit_new_admin_login.clear()
        self.lineEdit_new_admin_password.clear()
        self.get_info_from_db()
        return self.fill_table(self.info_for_search)

    def delete_admin(self):
        try:
            selected_rows = self.tableWidget.selectedItems()
            if not selected_rows:
                return

            selected_ids = set(self.tableWidget.item(row.row(), 0).text() for row in selected_rows)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Удаление пользователя')
            msg.setText("Вы уверены, что хотите удалить пользователя(лей)?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            btn = msg.exec_()
            if btn == QtWidgets.QMessageBox.Ok:
                for selected_id in selected_ids:
                    print(selected_id)
                    self.cursor.execute(f"DELETE FROM Users WHERE id = ?", [selected_id])
            self.db.commit()
            self.get_info_from_db()
            self.fill_table(self.info_for_search)

        except Exception as e:
            traceback.print_exc()

    def change_data(self):
        selected_fields = self.tableWidget.selectedItems()
        columns = {'Имя(login)': 'login', 'Пароль': 'password'}
        if not selected_fields:
            return

        for field in selected_fields:
            row = field.row()
            column = field.column()
            new_value = field.text()
            user_id = self.tableWidget.item(row, 0).text()
            col_name = columns[self.tableWidget.horizontalHeaderItem(column).text()]

            self.cursor.execute(
                f"UPDATE Users SET {col_name} = ? WHERE id = ?", [new_value, user_id])
        self.db.commit()
        self.get_info_from_db()
        self.fill_table(self.info_for_search)
