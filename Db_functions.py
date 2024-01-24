import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.db_file = 'Warehouses_db.db'
        self.db = sql.connect(self.db_file)

    def log_in(self, login, password):
        """Вход в приложение базы пользователем
        :param login: логин
        :param password: пароль
        :return: True - вход успешно выполнен, False - неверный логин или пароль"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT login, password
                                  FROM Users
                                  WHERE login = ? AND password = ?''', [login, password])
                result = cursor.fetchone()
                return True if result is not None else False
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_warehouse_info(self, warehouse):
        """Вход в приложение базы пользователем
        :param warehouse: название склада
        :return: True - склад найден, False - такого склада не существует"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT *
                                  FROM Warehouses
                                  WHERE warehouse_name = ?''', [warehouse])
                result = cursor.fetchone()
                return True if result is not None else False
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False
