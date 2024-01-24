import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.db_file = 'Warehouses_db.db'
        self.db = sql.connect(self.db_file)

    def log_in(self, login, password):
        """Вход в приложение базы пользователем
        :param login: логин, password: пароль
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

    def get_warehouses_names(self):
        """Получение всех названий складов
        :return: лист названий складов, пример: ['Запчасть плюс', 'Готовое и спелое']"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT warehouse_name
                                  FROM Warehouses''')
                result = cursor.fetchall()
                return [i[0] for i in result]
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_warehouse_info(self, warehouse):
        """Вход в приложение базы пользователем
        :param warehouse: название склада
        :return: возвращает список с кортежами каждого товара (id, категория, название, колличество, ед. изм.,
                 цена, дата изготовления, годен до, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT G.id, category_name, good_name, amount, measure_unit, price, time_start, 
                                         time_to_end, description, article_number, image
                                  FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                               JOIN Categories C ON G.category_id = C.id
                                  WHERE warehouse_name = ?''', [warehouse])
                result = cursor.fetchall()
                return result
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False


# DataBase().get_all_warehouses_names()
