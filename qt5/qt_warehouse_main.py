from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial

from qt5 import qt_make_order
from qt5 import qt_add_good
from qt5 import qt_edit_goods
from qt5 import qt_orders_history
from qt5 import qt_admin_panel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(730, 435)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox_warehouses = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_warehouses.setGeometry(QtCore.QRect(30, 10, 300, 20))
        self.comboBox_warehouses.setCurrentText("")
        self.comboBox_warehouses.setObjectName("comboBox_warehouses")
        self.table_warehouse = QtWidgets.QTableView(self.centralwidget)
        self.table_warehouse.setGeometry(QtCore.QRect(30, 60, 670, 330))
        self.table_warehouse.setObjectName("table_warehouse")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setGeometry(QtCore.QRect(530, 10, 170, 30))
        self.lineEdit_search.setText("")
        self.lineEdit_search.setFrame(False)
        self.lineEdit_search.setObjectName("lineEdit_search")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar_warehouse = QtWidgets.QMenuBar(MainWindow)
        self.menubar_warehouse.setGeometry(QtCore.QRect(0, 0, 730, 20))
        self.menubar_warehouse.setObjectName("menubar_warehouse")
        self.menu = QtWidgets.QMenu(self.menubar_warehouse)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar_warehouse)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.action_5)
        self.menubar_warehouse.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выбор склада"))
        self.lineEdit_search.setPlaceholderText(_translate("MainWindow", "Поиск..."))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.action.setText(_translate("MainWindow", "Оформить заказ"))
        self.action_2.setText(_translate("MainWindow", "Добавить товар"))
        self.action_3.setText(_translate("MainWindow", "Редактировать товары"))
        self.action_4.setText(_translate("MainWindow", "История заказов"))
        self.action_5.setText(_translate("MainWindow", "Панель администратора"))
        self.action.triggered.connect(partial(self.open_window, qt_make_order.Ui_make_order()))
        self.action_2.triggered.connect(partial(self.open_window, qt_add_good.Ui_add_good()))
        self.action_3.triggered.connect(partial(self.open_window, qt_edit_goods.Ui_Edit_goods()))
        self.action_4.triggered.connect(partial(self.open_window, qt_orders_history.Ui_Orders_History()))
        self.action_5.triggered.connect(partial(self.open_window, qt_admin_panel.Ui_Admin_panel()))

    def open_window(self, window):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = window
        self.ui.setupUi(self.main_window)
        self.main_window.show()
