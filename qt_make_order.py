import sqlite3
import traceback
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5.QtGui import QPixmap

import qt_cart


class Ui_make_order(object):
    def __init__(self, user):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()
        self.selected_warehouse = None
        self.cart_count = 0
        self.goods_in_cart = []
        self.current_window = None
        self.current_user = user

    def setupUi(self, make_order):
        make_order.setObjectName("make_order")
        make_order.resize(700, 394)
        self.btn_cart = QtWidgets.QPushButton(make_order)
        self.btn_cart.setGeometry(QtCore.QRect(500, 350, 190, 30))
        self.btn_cart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_cart.setObjectName("btn_cart")
        self.btn_add_to_cart = QtWidgets.QPushButton(make_order)
        self.btn_add_to_cart.setGeometry(QtCore.QRect(10, 350, 190, 30))
        self.btn_add_to_cart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_to_cart.setObjectName("btn_add_to_cart")
        self.lineEdit_search_order = QtWidgets.QLineEdit(make_order)
        self.lineEdit_search_order.setGeometry(QtCore.QRect(490, 320, 200, 20))
        self.lineEdit_search_order.setFrame(False)
        self.lineEdit_search_order.setObjectName("lineEdit_search_order")
        self.lineEdit_quantity = QtWidgets.QLineEdit(make_order)
        self.lineEdit_quantity.setGeometry(QtCore.QRect(110, 320, 50, 20))
        self.lineEdit_quantity.setFrame(False)
        self.lineEdit_quantity.setObjectName("lineEdit_quantity")
        self.lineEdit_quantity.setText("1")
        self.label_quantity = QtWidgets.QLabel(make_order)
        self.label_quantity.setGeometry(QtCore.QRect(20, 320, 70, 20))
        self.label_quantity.setObjectName("label_quantity")
        self.table_make_order = QtWidgets.QTableWidget(make_order)
        self.table_make_order.setGeometry(QtCore.QRect(10, 20, 680, 290))
        self.table_make_order.setObjectName("table_make_order")

        self.show_data()
        make_order.closeEvent = self.close_window

        self.retranslateUi(make_order)
        QtCore.QMetaObject.connectSlotsByName(make_order)

    def retranslateUi(self, make_order):
        _translate = QtCore.QCoreApplication.translate
        make_order.setWindowTitle(_translate("make_order", "Оформление заказа"))
        self.btn_cart.setText(_translate("make_order", "Корзина"))
        self.btn_add_to_cart.setText(_translate("make_order", "Добавить в корзину"))
        self.lineEdit_search_order.setPlaceholderText(_translate("make_order", "Поиск..."))
        self.label_quantity.setText(_translate("make_order", "Колличество:"))
        self.lineEdit_search_order.returnPressed.connect(partial(self.show_data))
        self.btn_add_to_cart.clicked.connect(partial(self.add_to_cart))
        QtCore.QMetaObject.connectSlotsByName(make_order)
        self.btn_cart.clicked.connect(partial(self.open_window, qt_cart.Ui_Cart(self, self.current_user)))

    def show_data(self, selected_warehouse_data=None):
        if selected_warehouse_data is None:
            search_text = self.lineEdit_search_order.text()
            if search_text:
                self.cursor.execute(f"""SELECT good_name, amount, measure_unit, price, time_start, time_to_end,
                description, article_number, image FROM Goods WHERE LOWER(good_name) LIKE LOWER(?)""",
                                    [f"%{search_text}%"])
            else:
                self.cursor.execute("""SELECT good_name, amount, measure_unit, price, time_start, time_to_end,
                description, article_number, image FROM Goods""")
            res = self.cursor.fetchall()
            if not res:
                QtWidgets.QMessageBox.information(self.table_make_order, 'Поиск товаров', 'Данные не найдены!')
            else:
                self.fill_table(res)
        else:
            self.fill_table(selected_warehouse_data)

    def fill_table(self, info):
        col_names = ['Название', 'Количество', 'Единица измер.', 'Цена', 'Годен с', 'Годен до', 'Описание',
                     'Артикль', 'Изображение']
        self.table_make_order.setRowCount(0)
        self.table_make_order.setColumnCount(len(info[0]))
        self.table_make_order.setHorizontalHeaderLabels(col_names)
        for row_number, row_data in enumerate(info):
            self.table_make_order.insertRow(row_number)
            for column, data in enumerate(row_data):
                if column == len(row_data)-1:
                    button = QPushButton()
                    button.setText("Открыть")
                    button.clicked.connect(partial(self.open_image, data))
                    self.table_make_order.setCellWidget(row_number, column, button)
                if column == len(row_data) - 2:
                    item = QtWidgets.QTableWidgetItem(str(data))
                    if column == len(row_data) - 2:
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                        self.table_make_order.setItem(row_number, column, item)
                else:
                    item = QtWidgets.QTableWidgetItem(str(data))
                    self.table_make_order.setItem(row_number, column, item)


    def open_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
            self.image_label = QtWidgets.QLabel()
            self.image_label.setPixmap(pixmap)
            self.image_label.setWindowTitle("Изображение")
            self.image_label.show()

    def add_to_cart(self):
        quantity = self.lineEdit_quantity.text()
        if not quantity.isdigit() or quantity.startswith('0') or quantity.strip() == '':
            return QtWidgets.QMessageBox.warning(self.table_make_order, 'Ошибка', 'Некорректное количество товара!')

        selected_field = self.table_make_order.selectedRanges()[-1]
        if selected_field:
            selected_field = selected_field.bottomRow() + 1
        if not selected_field:
            return QtWidgets.QMessageBox.warning(self.table_make_order, 'Ошибка', 'Выберите товар!')

        article = self.table_make_order.item(selected_field - 1, 7).text()
        self.cursor.execute("SELECT amount FROM Goods WHERE article_number = ?", [article])
        good_quantity = self.cursor.fetchone()[0]

        if float(quantity) > float(good_quantity):
            return QtWidgets.QMessageBox.warning(self.table_make_order, 'Ошибка', 'Недопустимое количество товара!')

        article = self.table_make_order.item(selected_field - 1, 7).text()
        self.goods_in_cart.append([article, quantity])

        self.cart_count += 1
        self.delete_for_cart(article, int(quantity))
        self.lineEdit_quantity.setText('1')
        _translate = QtCore.QCoreApplication.translate
        self.btn_cart.setText(_translate("make_order", f"Корзина {self.cart_count}"))

    def delete_for_cart(self, good_article, quantity_for_delete):
        try:
            self.cursor.execute(f"SELECT amount FROM Goods WHERE article_number = ?", [good_article])
            first_quantity = int(self.cursor.fetchone()[0])
            self.cursor.execute(f"UPDATE Goods SET amount = ? WHERE article_number = ?",
                                [first_quantity - quantity_for_delete, good_article])
            self.db.commit()
            self.show_data()

        except Exception as e:
            traceback.print_exc()

    def close_window(self, event):
        for good in self.goods_in_cart:
            self.cursor.execute(f"SELECT amount FROM Goods WHERE article_number = ?", [int(good[0])])
            current_quantity = int(self.cursor.fetchone()[0])
            self.cursor.execute(f"UPDATE Goods SET amount = ? WHERE article_number = ?",
                                [current_quantity + int(good[1]), int(good[0])])
        self.db.commit()
        self.goods_in_cart = []
        self.cart_count = 0
        event.accept()

    def open_window(self, window):
        if len(self.goods_in_cart) == 0:
            QtWidgets.QMessageBox.information(self.table_make_order, 'Ошибка', 'Товары не найдены')
            return
        self.current_window = QtWidgets.QApplication.activeWindow()
        self.main_window = QtWidgets.QMainWindow()
        self.ui = window
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.current_window.hide()



