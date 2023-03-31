import sqlite3
from sqlite3 import Error
import datetime
import random

ID = 0
final = False
tovar_order = True
singin = True
brek = False
order_final = False
dostup = False
sty = ""
final_price = 0
final_count = 0
order_list = list()

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
connection = create_connection("C:\\Users\\alert\\Documents\\mptpy\\P50-7-20 Efimenko\\PR3\\sm_app.sqlite")

def execute_query(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully") 
    except Error as e:
        print(f"The error '{e}' occurred")

def select_table(query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def authorization(login, password):
    global ID, dostup, singin, sty, brek
    for user in users:
        if(user[4] == login and user[5] == password):
            print("NICE!")
            singin = False
            dostup = True
            ID = user[0]
            brek = True
            sty = "user"
            break
        else:
            sty = ""
            singin = True
            dostup = False
            ID = 0
    if(brek == False):
        for admin in admins:
            if(admin[6] == login and admin[7] == password):
                print("NICE")
                dostup = True
                singin = False
                ID = admin[0]
                sty = "admin"
                break
            else:
                sty = ""
                singin = True
                dostup = False
                ID = 0

    

def order():
    global final_price, final_count, order_final
    print("Выберите действие:")
    print("~1 - Готовые блюда")
    print("~2 - Конструктор")
    print("~3 - Акции")
    print("~4 - Отменить заказ")
    print("")
    b = int(input("= "))
    if(b == 1):
        i = 0
        for product in products:
            if(i == 0):
                print(f"Название: {product[1]}")
                print(f"Цена: {product[3]}")
                print("Состав:")
                price = product[3]
            print(f"{product[5]}")
            i = i + 1
        while order_final == False:
            print("")
            count = int(input("Выберите кол-во: "))
            print("")
            all_count = 0
            count_sources = 0
            for source in sources:
                count_sources += 1
                all_count += source[2]
            if(count * count_sources > all_count):
                print("Невозможно заказать столько!")
            else:
                order_final = True
        order_final = False
        final_count += count
        final_price += price * count
        print(f"Цена вашего заказа: {final_price}")
        oplata = int(input("Перейти к оплате: 1 - ДА, 2 - НЕТ "))
        print("")
        if(oplata == 1):
            print(f"С вас {final_price} рублей.")
            сoplata = int(input("Оплатить: 1 - ДА, 2 - НЕТ "))
            print("")
            if(сoplata == 1):
                for user in users:
                    if(ID == user[0]):
                        if(user[6] >= final_price):
                            execute_query(f"UPDATE users SET score_users = {user[6] - final_price} WHERE id_users = {user[0]};")
                        else:
                            print("На вашем счету нету средств!")
                            final_price = 0
                            final_count = 0
                            menu()
                soctav = ""
                for product in products:
                    soctav += f":{product[5]}:"
                oplatil(product[1], soctav)
            if(сoplata == 2):
                menu()
        if(oplata == 2):
            menu()
    elif(b == 2):
        soctav = ""
        for product in products:
            print(f"Навание: {product[1]}")
            break
        for source in sources:
            print(f"Хотите добавить {source[1]}?")
            op = int(input("1 - Да, 2 - Нет "))
            if(op == 1):
                soctav += f":{source[1]}:"
                while order_final == False:
                    print("Введите сколько хотите дабавить")
                    opa = int(input("= "))
                    if(opa > source[2]):
                        print("Невозможно столько добавить!")
                    else:
                        final_price += source[3] * opa
                        order_final = True
                order_final = False
            elif(op == 2):
                print("")
            else:
                print("Вы вили не то число!")
        print("Введите сколько хотите добавить таких блюд")
        opach = int(input("= "))
        print(f"Цена вашего заказа: {final_price}")
        oplata = int(input("Перейти к оплате: 1 - ДА, 2 - НЕТ "))
        if(oplata == 1):
            print(f"С вас {final_price} рублей.")
            сoplata = int(input("Оплатить: 1 - ДА, 2 - НЕТ "))
            print("")
            if(сoplata == 1):
                for user in users:
                    if(ID == user[0]):
                        if(user[6] >= final_price):
                            execute_query(f"UPDATE users SET score_users = {user[6] - final_price} WHERE id_users = {user[0]};")
                        else:
                            print("На вашем счету нету средств!")
                            final_price = 0
                            final_count = 0
                            menu()
                oplatil(product[1], soctav)
            if(сoplata == 2):
                menu()
        if(oplata == 2):
            menu()
    elif(b == 3):
        b
    elif(b == 4):
        final_price = 0
        final_count = 0
    else:
        print("Вы вили не то число!")

def oplatil(productis, soctavs):
    global final_price, final_count
    for admin in admins:
            if(1 == admin[0]):
                execute_query(f"UPDATE admins SET score_admins = {admin[8] + final_price} WHERE id_admin = {admin[0]};")
    for user in users:
        if(ID == user[0]):
            if not user[7]:
                break
            else:
                final_price -= final_price / 100 * user[11]
                print(f"Ваша скидка {user[11]}")
                print("")
                break
    rand_eye = random.randint(0, 2)
    rand_users = random.randint(0, 4)
    if(rand_eye == 2):
        print("Не видно пользователю! В рулете глаз!")
        if(rand_users == rand_eye):
            print("Мммм... Вкусный глаз!")
            soctavs += ", Глаз"
            final_price -= final_price / 100 * 30
        else:
            print("Вы ничего не заметели!")
    order_list.append(f"Название: {productis} | Состав: {soctavs} | Кол-во: {final_count}")
    print("Ваш чек:")
    print(datetime.datetime.now())
    print(f"{order_list[-1]} | Цена: {final_price}")
    print("")
    execute_query(f"INSERT INTO history (datatime_history, item_history, price_history, users_id) VALUES ('{datetime.datetime.now()}', '{order_list[-1]}', {final_price}, {ID});")
    for card in cards:
        if(final_price < 5000):
            break
        if(final_price < card[2]):
            execute_query(f"UPDATE users SET cards = {card[2] - 1} WHERE id_users = {ID};")
    final_price = 0
    final_count = 0

def menu():
    global final
    print("")
    print("Нажмите цифру от 1 до * для навигации:")
    print("~1 - Информация")
    print("~2 - Заказ")
    print("~3 - Выйти")
    a = int(input("= "))
    print("")
    if(a == 1):
        for user in users:
            if(user[0] == ID):
                print(f"ФИО: {user[1]} {user[2]} {user[3]}")
                print(f"Login: {user[4]} | Password: {user[5]}")
                print(f"Счет: {user[6]}")
                print(f"Карта: {user[9]} | Скидка: {user[11]}")
                print("")
                print("~1 - Посмотреть историю")
                tyu = int(input("= "))
                if(tyu == 1):
                    print(select_table(f"SELECT * FROM history WHERE users_id = {user[0]}"))
                else:
                    print("Вы вили не то число!")
                break
    elif(a == 2):
        order()
    elif(a == 3):
        final = True
    else:
        print("Вы вили не то число!")

def admin():
    global final, final_price, tovar_order
    for admin in admins:
        if(ID == admin[0]):
            print(f"Счет: {admin[8]}")
            break
    print("")
    print("Нажмите цифру от 1 до * для навигации:")
    print("~1 - Посмотреть историю пользователя")
    print("~2 - Купить товары")
    print("~3 - Выйти")
    a = int(input("= "))
    print("")
    if(a == 1):
        num = int(input("Введите номер: "))
        for user in users:
            if(user[0] == num):
                print(select_table(f"SELECT * FROM history WHERE users_id = {user[0]}"))
                break
    elif(a == 2):
        while tovar_order == True:
            print(sources)
            print("")
            tovar = int(input("Выберите товар из списка: "))
            print("")
            for sour in sources:
                if(tovar == sour[0]):
                    tru = True
                    while tru == True:
                        cen = int(input("Введите сколько хотите купить: "))
                        if(cen > sour[2]):
                            print("Вы ввели не правильное число")
                        else:
                            tru = False
                    execute_query(f"UPDATE sources SET count_sources = {sour[2] + cen} WHERE id_sources = {sour[0]};")
                    final_price += sour[3] * cen
                    print("Продолжить закупку?")
                    jo = int(input("1 - Да, 2 - Нет "))
                    if(jo == 1):
                        jo = 0
                        break
                    elif(jo == 2):
                        tovar_order = False
                    else:
                        print("Вы вили не то число!")
                else:
                    print("Такого товара нет!")
        tovar_order == True
        for admin in admins:
            if(ID == admin[0]):
                execute_query(f"UPDATE admins SET score_admins = {admin[8] - final_price} WHERE id_admin = {admin[0]};")
    elif(a == 3):
        final = True
    else:
        print("Вы вили не то число!")

users = select_table(f"SELECT * FROM users INNER JOIN cards ON cards.id_cards = users.cards_id")
admins = select_table("SELECT * FROM admins")
sources = select_table("SELECT * FROM sources")
products = select_table("SELECT * FROM products INNER JOIN sources ON sources.id_sources = products.sources_id")
cards = select_table(f"SELECT * FROM cards")

print("Добро пожаловать в Рулет у Бреда!")
while singin == True:
    log = input("Login: ")
    pas = input("Password: ")
    authorization(log, pas)

if(dostup == True):
    while final == False:
        if(sty == "user"):
            menu()
        if(sty == "admin"):
            admin()

print(users)