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

    def get_warehouse_info(self, warehouse_name):
        """Получение информации о товарах на складе
        :param warehouse_name: название склада
        :return: возвращает список с кортежами каждого товара (id, категория, название, количество, ед. изм.,
                 цена, дата изготовления, годен до, описание, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT G.id, category_name, good_name, amount, measure_unit, price, time_start, 
                                         time_to_end, description, article_number, image
                                  FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                               JOIN Categories C ON G.category_id = C.id
                                  WHERE warehouse_name = ?''', [warehouse_name])
                result = cursor.fetchall()
                return result
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_good_into_db(self, good_info):
        """Добавление нового товара на склад
        :param good_info: [название склада (текущий) (str), категория (str), название товара (str),
                           количество (int), ед. изм. (str), цена (int), дата изготовления (str),
                           годен до (str), описание (str), артикул (int), путь к фото (str)]
        :return: True - товар добавлен, False - описание ошибки"""
        try:
            with self.db:
                '''Проверка на наличие категории/добавление и получение id категории'''
                cursor = self.db.cursor()
                cursor.execute('''SELECT id
                                  FROM Categories
                                  WHERE category_name = ?''', [good_info[1]])
                categ_id = cursor.fetchone()
                if categ_id is not None:
                    good_info[1] = categ_id
                else:
                    cursor.execute('''INSERT INTO Categories (category_name)
                                      VALUES (?)''', [good_info[1]])
                    cursor.execute('''SELECT MAX(id)
                                      FROM Categories''')
                    # cursor.execute('''SELECT id
                    #                   FROM Categories
                    #                   WHERE category_name = ?''', [good_info[1]])
                    good_info[1] = cursor.fetchone()
                cursor.execute('''SELECT id
                                  FROM Warehouses
                                  WHERE warehouse_name = ?''', [good_info[0]])
                good_info[0] = cursor.fetchone()
                good_info[0], good_info[1] = good_info[1][0], good_info[0][0]  # из кортежа в число

                cursor.execute('''INSERT INTO Goods(warehouse_id, category_id, good_name, amount, measure_unit,
                                  price, time_start, time_to_end, description, article_number, image)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', good_info)
                return cursor.rowcount > 0
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False


#DataBase().add_new_good_into_db(["Запчасть плюс", "Проgdgdдукffaт;ы", "1", 1, "1", 1, "1", "1", "1", 1, "1"])
