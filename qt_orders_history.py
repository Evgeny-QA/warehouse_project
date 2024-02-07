from PyQt5 import QtCore, QtGui, QtWidgets
from Db_functions import DataBase
from PyQt5.QtWidgets import QPushButton, QWidget
from os import startfile
from functools import partial


class Ui_Orders_History(object):
    def __init__(self, user):
        self.current_user = user
        self.flag = False

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

        self.tableWidget_table_history.horizontalHeader().sectionClicked.connect(self.sort_table)

        self.retranslateUi(Orders_History)
        QtCore.QMetaObject.connectSlotsByName(Orders_History)

        table_collums = ["№ Заказа", "Составитель ТТН", "Компания (заказчик)",
                         "Адрес доставки", "Word", "Excel", "Товары"]
        self.tableWidget_table_history.setColumnCount(len(table_collums))
        self.tableWidget_table_history.setHorizontalHeaderLabels(table_collums)
        self.fill_table()

    def retranslateUi(self, Orders_History):
        _translate = QtCore.QCoreApplication.translate
        Orders_History.setWindowTitle(_translate("Orders_History", "История заказов"))
        self.lineEdit.setPlaceholderText(_translate("Orders_History", "Поиск..."))
        self.lineEdit.returnPressed.connect(self.fill_table)

    # сортировака по столбикам
    def sort_table(self, column):
        if not self.flag or self.tableWidget_table_history.horizontalHeader().sortIndicatorSection() != column:
            self.tableWidget_table_history.sortItems(column, QtCore.Qt.AscendingOrder)
            self.flag = True
        else:
            self.tableWidget_table_history.sortItems(column, QtCore.Qt.DescendingOrder)
            self.flag = False

    def open_window_goods_info(self, order_id):
        self.window_order_info = QWidget()
        self.window_order_info.setWindowTitle('Новое окно')
        self.window_order_info.setObjectName("Admin_panel")
        self.window_order_info.setWindowModality(QtCore.Qt.NonModal)
        self.tableWidget1 = QtWidgets.QTableWidget(self.window_order_info)
        self.tableWidget1.setGeometry(QtCore.QRect(20, 20, 335, 300))
        self.tableWidget1.setObjectName("tableView_data")
        self.window_order_info.resize(375, 335)
        self.window_order_info.show()
        self.window_order_info.setWindowTitle(QtCore.QCoreApplication.translate("window_order_info", "Товары заказа"))

        table_collums = ["Название", "ед. изм.", "Количество"]
        self.tableWidget1.setColumnCount(len(table_collums))
        self.tableWidget1.setHorizontalHeaderLabels(table_collums)
        self.fill_table(order_id)

    def input_file_button(self, row, coll, file_text, file_path):
        button = QPushButton()
        button.setText(file_text)
        button.clicked.connect(partial(startfile, file_path))
        self.tableWidget_table_history.setCellWidget(row, coll, button)

    def fill_table(self, order_id=None):
        if order_id is None:
            search_text = self.lineEdit.text().lower()
            info_for_search = DataBase().get_completed_orders()

            if search_text:
                info = []
                for i in info_for_search:
                    if i[2].lower() == search_text or search_text in i[2].lower() or search_text in i[1].lower():
                        info.append(i)
                if len(info) == 0:
                    QtWidgets.QMessageBox.information(self.tableWidget_table_history, 'Ошибка поиска', 'Данные не найдены!')
                    return
            else:
                info = info_for_search
            self.tableWidget_table_history.setRowCount(len(info))
            for row, str_info in enumerate(info):
                len_str = len(str_info)
                order_id = ""
                for coll, info_insert in enumerate(str_info):
                    if not order_id:
                        order_id = info_insert
                    if coll == len_str - 2:
                        self.input_file_button(row, coll, "Word", info_insert)
                    elif coll == len_str - 1:
                        self.input_file_button(row, coll, "Excel", info_insert)
                        button = QPushButton()
                        button.setText("Посмотреть")
                        button.clicked.connect(partial(self.open_window_goods_info, order_id))
                        self.tableWidget_table_history.setCellWidget(row, coll + 1, button)
                    else:
                        self.tableWidget_table_history.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))
        else:
            info = DataBase().get_goods_info_from_order(order_id)
            if len(info) == 0:
                QtWidgets.QMessageBox.information(self.tableWidget1, 'Ошибка поиска', 'Данные не найдены!')
                return
            self.tableWidget1.setRowCount(len(info))
            for row, str_info in enumerate(info):
                for coll, info_insert in enumerate(str_info):
                    self.tableWidget1.setItem(row, coll, QtWidgets.QTableWidgetItem(str(info_insert)))

