import sqlite3
#from tkinter import *
import tkinter as tk
from tkinter import messagebox


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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stacked Widget Example")
        self.geometry("1440x720")

        # Container to hold all the pages
        self.container = tk.Frame(self)
        self.container.pack(fill="y")

        
        

        # Dictionary to hold the pages
        self.pages = {}

        # Initialize the pages
        for PageClass in (LoginPage, HomePage):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky='nsew')

        # Show the initial page
        self.show_page("LoginPage")

    def show_page(self, page_name):
        """Bring the page with the given name to the front."""
        page = self.pages[page_name]
        page.tkraise()
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Frame(self).pack(fill='y', expand=True,pady=100)

        tk.Label(self, text='Логин:').pack(pady=20,anchor='center')
        tk.Label(self, text="Username:").pack(pady=5)
        self.login_txt = tk.Entry(self)
        self.login_txt.pack(pady=5)
        
        tk.Label(self, text="Password:").pack(pady=5)
        self.password_txt= tk.Entry(self, show="*")
        self.password_txt.pack(pady=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=20)
    
    def login(self):
        input_login = self.login_txt.get()
        input_password = self.password_txt.get()
        if (input_login == 'admin') and (input_password == 'admin'):
            self.controller.show_page("HomePage")
        else:
            messagebox.showerror("Title", "Message")
            print('Данные не верные, повторите попытку или обратитесь к системному администратору')

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.container = tk.Frame(self)
        self.container.pack(fill="none")
        self.controller = controller
        tk.Button(self, text='Сотрудники',command=show_users, width=30, height=3).pack(fill='x', padx=40,pady=50, anchor='w')
        tk.Button(self, text='Оборудование',command=show_equip, width=30, height=3).pack(fill='x', padx=40,pady=50, anchor='w')
        tk.Button(self, text='Офис',command=show_office, width=30, height=3).pack(fill='x', padx=40,pady=50, anchor='w')
        
    # choose_db = input('1) Сотрудники\n2) Оборудование\n3) Офисы')
    # if choose_db == '1':
    #     data = 'users'
    # elif choose_db == '2':
    #     data = 'equipment'
    # elif choose_db == '3':
    #     data = 'office'
    # else:
    #     print('Неверные данные')
    #     main_menu()
def show_users(self):
    # window = tk.Tk()
    # window.state("zoomed")
    listbox = tk.Listbox(self)
    listbox.pack()
    try:
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        for i in cursor.execute(f'SELECT * FROM users'):
            listbox.insert(tk.END, i)
            print(i)
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        print('Открыта таблица сотрудников')

def show_equip():
    try:
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        for i in cursor.execute(f'SELECT * FROM equipment'):
            print(i)
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        print('Открыта таблица оборудования')
    
def show_office():
    try:
        dp = sqlite3.connect('database.db')
        cursor = db.cursor()

        for i in cursor.execute(f'SELECT * FROM office'):
            print(i)
    except sqlite3.Error as e:
        print('Error',e)
    finally:
        print('Открыта таблица офисов')

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
            
if __name__ == "__main__":
    app = App()
    app.mainloop()

