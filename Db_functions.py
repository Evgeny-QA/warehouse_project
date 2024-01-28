import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.db_file = 'Warehouses_db.db'
        self.db = sql.connect(self.db_file)

    def log_in(self, login):  # 27 log_in
        """Вход в приложение базы пользователем
        :param login: логин
        :return: Возвращает пароль, если пароль не верный - None"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT password 
                                  FROM users 
                                  WHERE login=?''', [login])
                password = cursor.fetchone()
                return password
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
                names = cursor.fetchall()
                return [i[0] for i in names]
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_all_goods_from_warehouses(self, search_text):  # 115 строка qt_warehouse_main
        """Получение информации о всех товарах на всех складах
        :return: возвращает все товары на всех складах (склад, категория, название, количество, ед. изм.,
                 цена, дата изготовления, годен до, описание, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                if search_text:
                    cursor.execute('''SELECT warehouse_name, category_name, good_name, amount, measure_unit, price, 
                                             time_start, time_to_end, description, article_number, image 
                                      FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                                   JOIN Categories C ON G.category_id = C.id
                                      WHERE LOWER(good_name) LIKE LOWER(?)''', [f"%{search_text}%"])
                else:
                    cursor.execute('''SELECT warehouse_name, category_name, good_name, amount, measure_unit, price, 
                                             time_start, time_to_end, description, article_number, image 
                                      FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                                   JOIN Categories C ON G.category_id = C.id''')

                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_goods_from_warehouse(self, warehouse_name, search_text):  # 140 строка qt_warehouse_main
        """Получение информации о товарах на определенном складе
        :param warehouse_name: название склада
        :return: возвращает список с кортежами каждого товара (категория, название, количество, ед. изм.,
                 цена, дата изготовления, годен до, описание, артикул, путь к фото)"""
        try:
            with self.db:
                cursor = self.db.cursor()
                if search_text:
                    cursor.execute('''SELECT category_name, good_name, amount, measure_unit, price, time_start, 
                                             time_to_end, description, article_number, image
                                      FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                                   JOIN Categories C ON G.category_id = C.id
                                      WHERE warehouse_name = ? AND LOWER(good_name) LIKE LOWER(?)''',
                                   [warehouse_name, f"%{search_text}%"])
                else:
                    cursor.execute('''SELECT category_name, good_name, amount, measure_unit, price, time_start, 
                                             time_to_end, description, article_number, image
                                      FROM Goods G JOIN Warehouses W ON G.warehouse_id = W.id 
                                                   JOIN Categories C ON G.category_id = C.id
                                      WHERE warehouse_name = ?''', [warehouse_name])
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_good_into_db(self, good_info):
        """Добавление нового товара на склад
        :param good_info: [название склада (str), категория (str), название товара (str),
                           количество (int), ед. изм. (str), цена (int), дата изготовления (str),
                           годен до (str), описание (str), артикул (int), путь к фото (str)]
        :return: True - товар добавлен"""
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


DataBase().add_new_good_into_db(["Запчасть плюс", "Проgdgdдукffaт;ы", "1", 1, "1", 1, "1", "1", "1", 1, "1"])
