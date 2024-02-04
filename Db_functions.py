import sqlite3 as sql
from datetime import date

class DataBase:
    def __init__(self):
        self.db_file = 'Warehouses_db.db'
        self.db = sql.connect(self.db_file)

    '''log_in'''
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

    '''all files'''
    def get_all_goods_from_warehouses(self, search_text):  # 115 строка qt_warehouse_main 62 qt_add_good 66 qt_edit_goods
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

    '''qt_warehouse_main'''
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

    '''qt_add_good'''
    def get_all_categories(self):  # 96 qt_add_good
        """Получение всех доступных категорий товаров
        :return: Возвращает все категории товаров"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT category_name 
                                  FROM Categories''')
                categories = cursor.fetchone()
                return categories
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def add_new_good_into_db(self, good_info):  # 178 qt_add_good
        """Добавление нового товара на склад
        :param good_info: [название склада (str), категория (str), название товара (str),
                           количество (int), ед. изм. (str), цена (int), дата изготовления (str),
                           годен до (str), описание (str), путь к фото (str)]
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
                                                    price, time_start, time_to_end, description, image)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', good_info)
                return cursor.rowcount > 0
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_edit_goods'''
    def delete_good(self, article_id):  # 124 qt_edit_goods
        """Удаление товара со склада
        :param article_id - номер товара"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''DELETE FROM Goods 
                                  WHERE article_number = ?''', [article_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_admin_panel'''
    def add_new_user(self, login, password):  # 86
        """Добавление пользователя
        :param login - логин нового пользователя, password - пароль нового пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''INSERT INTO Users(login, password) 
                                  VALUES(?,?)''', [login, password])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def update_user_info(self, login, password, user_id):  # 86
        """Обновление информации пользователя
        :param login - логин пользователя, password - пароль пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''UPDATE Users 
                                  SET login = ?, password = ? 
                                  WHERE id = ?''', [login, password, user_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def delete_user(self, user_id):  # 86
        """Удаление пользователя
        :param user_id - номер пользователя"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''DELETE FROM Users 
                                  WHERE id = ?''', [user_id])
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''schedule_delete_goods'''
    def delete_after_time_good_end(self):
        """Удаление товара со склада после окончания срока годности
        :return: Возвращает пароль, если пароль не верный"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''DELETE FROM Goods
                                  WHERE time_to_end IS NOT NULL 
                                  AND Cast ((JulianDay('now') - JulianDay(time_to_end)) as Integer) >= 0''')
                print("Delete done:" + str(date.today()))
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    '''qt_orders_history'''
    def get_completed_orders(self, search_text=None):
        """Получение всех заказов
        :return: Возвращает список заказов"""
        try:
            with self.db:
                cursor = self.db.cursor()
                if search_text not in (None, ""):
                    cursor.execute('''SELECT O.id, login, company_name, delivery_address, file_word, file_excel
                                      FROM Users U JOIN Orders O ON U.id = O.user_id JOIN Companies C ON 
                                                        O.company_id = C.id
                                      WHERE LOWER(company_name) LIKE LOWER(?)''', [f"%{search_text}%"])
                else:
                    cursor.execute('''SELECT O.id, login, company_name, delivery_address, file_word, file_excel
                                      FROM Users U JOIN Orders O ON U.id = O.user_id JOIN Companies C ON 
                                                        O.company_id = C.id''')
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False

    def get_goods_info_from_order(self, id):
        """Получение информации о товарах заказа
        :param id - ид заказа
        :return: Возвращает список информации о товарах заказа"""
        try:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('''SELECT good_name, measure_unit, GO.amount
                                  FROM Goods_in_order GO JOIN Goods G ON GO.good_id = G.article_number
                                  WHERE order_id = ?''', [id])
                info = cursor.fetchall()
                return info
        except sql.Error as error:
            print(f"Произошла ошибка: {error}")
            return False




# DataBase().get_completed_orders()


    '''ДЛЯ ОЛЕГА СОЗДАНИЕ word/excel'''
    # '''cart'''
    # def create_order_documets(self, ):
    #     """Удаление пользователя
    #     :param """
    #     try:
    #         with self.db:
    #             cursor = self.db.cursor()
    #             cursor.execute('''DELETE FROM Users
    #                                       WHERE id = ?''', [user_id])
    #     except sql.Error as error:
    #         print(f"Произошла ошибка: {error}")
    #         return False

# DataBase().add_new_user(0,0)
# DataBase().delete_good(222)
# DataBase().add_new_good_into_db(["Запчасть плюс", "Продуктыыыы", "1", 1, "1", 1, "1", "1", "1", "1"])
