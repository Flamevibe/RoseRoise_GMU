import sqlite3
from tkinter import *

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()

    cursor.executescript("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        surname VARCHAR,
        date INTEGER,
        work TEXT,
        office VARCHAR
    );
    CREATE TABLE IF NOT EXISTS equipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        number INTEGER,
        status VARCHAR,
        office VARCHAR
    );
    CREATE TABLE IF NOT EXISTS office(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city VARCHAR,
        address TEXT,
        `index` INTEGER
    )""")
def login():
    window = Tk() 
    window.geometry('400x250')
    login_admin = 'admin'
    password_admin = 'admin'
    txt = Entry(window,width=10) 
    txt.grid(column=1, row=0)
    input_login = input('Login: ')
    input_password = input('Password: ')
    if (input_login == login_admin) and (input_password == password_admin):
        print('Вы успешно вошли в систему!')
    else:
        print('Данные не верные, повторите попытку или обратитесь к системному администратору')
        return login()
    return main_menu()
        
def main_menu():
    data = ''
    choose_db = input('1) Сотрудники\n2) Оборудование\n3) Офисы')
    if choose_db == '1':
        data = 'users'
    elif choose_db == '2':
        data = 'equipment'
    elif choose_db == '3':
        data = 'office'
    else:
        print('Неверные данные')
        main_menu()
    return menu_base(data)

def menu_base(data):
    try:
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        for i in cursor.execute(f'SELECT * FROM {data}'):
            print(i)
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        cursor.close()
        db.close()
    return data

def reg_office():
    city = input('Город: ')
    address = input('Адрес: ')
    index = input('Индекс: ')
    
    try: 
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        cursor.execute("SELECT address FROM office WHERE address = ?", [address])
        if cursor.fetchone() is None:
            values = [city, address, index]
            cursor.execute("INSERT INTO office(city, address, `index`) VALUES(?, ?, ?)", values)
            db.commit()
        else:
            print("Данный офис уже зарегистрирован")
            reg_equip()
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        cursor.close()
        db.close()


def reg_equip():
    name = input('Название оборудования: ')
    number = input('Серийный номер: ')
    status = input('Статус: ')
    office = input('В какой офисе: ')
    
    try: 
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        cursor.execute("SELECT number FROM equipment WHERE number = ?", [number])
        if cursor.fetchone() is None:
            values = [name, number, status, office]
            cursor.execute("INSERT INTO equipment(name, number, status, office) VALUES(?, ?, ?, ?)", values)
            db.commit()
        else:
            print("Такое оборудование уже зарегистрированно")
            reg_equip()
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        cursor.close()
        db.close()



def reg_user():
    name = input('name: ')
    surname = input('surname: ')
    date = input('date of birth: ')
    work = input('work: ')
    office = input('office: ')

    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        cursor.execute("SELECT name and surname FROM users WHERE name = ? and surname = ?", [name, surname])
        if cursor.fetchone() is None:
            values = [name, surname, date, work, office]
            cursor.execute("INSERT INTO users(name, surname, age, work, office) VALUES(?, ?, ?, ?, ?)", values)
            db.commit()
        else:
            print("Такой сотрудник уже есть")
            reg_user()
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        cursor.close()
        db.close()


def delete(data):
    users_id = input('Введите ID для удаления из таблицы..')
    try:
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        print("Подключен к SQLite")

        cursor.execute(f"DELETE from {data} where id = ?", [users_id])
        db.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if db:
            db.close()
            print("Соединение с SQLite закрыто")
login()