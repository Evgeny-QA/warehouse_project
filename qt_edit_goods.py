import os
import shutil
import sqlite3
import traceback
from functools import partial
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QComboBox, QFileDialog
from PyQt5.QtGui import QPixmap

from Db_functions import DataBase as db


class Ui_Edit_goods(object):
    def __init__(self):
        self.db = sqlite3.connect('Warehouses_db.db')
        self.cursor = self.db.cursor()

    def setupUi(self, Edit_goods):
        Edit_goods.setObjectName("Edit_goods")
        Edit_goods.resize(700, 380)
        self.lineEdit_search = QtWidgets.QLineEdit(Edit_goods)
        self.lineEdit_search.setGeometry(QtCore.QRect(480, 20, 200, 30))
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.table_edit_goods = QtWidgets.QTableWidget(Edit_goods)
        self.table_edit_goods.setGeometry(QtCore.QRect(20, 60, 660, 250))
        self.table_edit_goods.setObjectName("table_edit_goods")
        self.layoutWidget = QtWidgets.QWidget(Edit_goods)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 310, 660, 60))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
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

        self.show_data_main()

        self.retranslateUi(Edit_goods)
        QtCore.QMetaObject.connectSlotsByName(Edit_goods)

    def retranslateUi(self, Edit_goods):
        _translate = QtCore.QCoreApplication.translate
        Edit_goods.setWindowTitle(_translate("Edit_goods", "Редактирование товаров"))
        self.lineEdit_search.setPlaceholderText(_translate("Edit_goods", "Поиск..."))
        self.btn_take_changes.setText(_translate("Edit_goods", "Подтвердить изменения"))
        self.btn_delete.setText(_translate("Edit_goods", "Удалить"))
        self.btn_cancel_changes.setText(_translate("Edit_goods", "Отменить изменения"))
        self.lineEdit_search.returnPressed.connect(partial(self.show_data_main))
        self.btn_delete.clicked.connect(partial(self.delete_good))
        self.btn_cancel_changes.clicked.connect(partial(self.show_data_main))

    def show_data_main(self):
        search_text = self.lineEdit_search.text()
        if search_text:
            self.cursor.execute(f"""SELECT good_name, amount, measure_unit, price, time_start, time_to_end,
            description, article_number, image FROM Goods WHERE LOWER(good_name) LIKE LOWER(?)""", [f"%{search_text}%"])
        else:
            self.cursor.execute("""SELECT good_name, amount, measure_unit, price, time_start, time_to_end,
            description, article_number, image FROM Goods""")
        res = self.cursor.fetchall()
        if not res:
            QtWidgets.QMessageBox.information(self.table_edit_goods, 'Поиск товаров', 'Данные не найдены!')
        else:
            self.fill_table(res)

    def fill_table(self, info):
        col_names = ['Название', 'Количество', 'Единица измер.', 'Цена', 'Годен с', 'Годен до', 'Описание',
                     'Артикль', 'Изображение']
        self.table_edit_goods.setRowCount(0)
        self.table_edit_goods.setColumnCount(len(info[0]))
        self.table_edit_goods.setHorizontalHeaderLabels(col_names)
        for row_number, row_data in enumerate(info):
            self.table_edit_goods.insertRow(row_number)
            for column, data in enumerate(row_data):
                if column == len(row_data)-1:
                    button = QPushButton()
                    button.setText("Открыть")
                    button.clicked.connect(partial(self.open_image, data))
                    self.table_edit_goods.setCellWidget(row_number, column, button)
                else:
                    self.table_edit_goods.setItem(row_number, column, QtWidgets.QTableWidgetItem(str(data)))

    def open_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
            self.image_label = QtWidgets.QLabel()
            self.image_label.setPixmap(pixmap)
            self.image_label.setWindowTitle("Изображение")
            self.image_label.show()

    def delete_good(self):
        try:
            selected_rows = self.table_edit_goods.selectedItems()
            if not selected_rows:
                return
            selected_ids = []
            for row in selected_rows:
                item = self.table_edit_goods.item(row.row(), 7)
                selected_ids.append(item.text())
            selected_ids = set(selected_ids)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle('Удаление товара')
            msg.setText("Вы уверены, что хотите удалить товар(ы)?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            btn = msg.exec_()
            if btn == QtWidgets.QMessageBox.Ok:
                for selected_id in selected_ids:
                    self.cursor.execute(f"DELETE FROM Goods WHERE article_number = ?", [selected_id])
            self.db.commit()
            self.show_data_main()

        except Exception as e:
            traceback.print_exc()




