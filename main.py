from nicegui import ui
import sqlite3
import webbrowser


ui.navigate.to('/login')
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
        owner VARCHAR,
        office VARCHAR
    );
    CREATE TABLE IF NOT EXISTS office(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city VARCHAR,
        address TEXT,
        oindex VARCHAR
    )""")



@ui.page('/')
def main_page() -> None:

    def logout() -> None:
        ui.navigate.to('/login')

    with ui.column().classes('absolute-center items-center'):
        ui.label('Hello admin!').classes('text-2xl')
        ui.button(on_click=logout, icon='logout').props('outline round')

@ui.page('/login')
def try_login() -> None:
    with ui.column().classes('absolute-center items-center'):
        ui.label('Войдите')
        txt_login = ui.input(label='Логин', placeholder='Введите логин').on('keydown.enter')
        txt_pass = ui.input(label='Пароль', placeholder='Введие пароль', password=True).on('keydown.enter')
        ui.button('Войти',
                  on_click=lambda: ui.navigate.to('/main') if txt_login.value == 'admin' and txt_pass.value == 'admin'
                  else ui.notify('Неверные данные', color='negative'))

 #@ui.page('/main')
# def main():
#     with ui.column().classes('justify-content-centert items-left'):
#         ui.add_css('''
#             :root {
#                 --nicegui-default-padding: 30px;
#                 --nicegui-default-gap: 3rem;
#             }
#         ''')
#         ui.button('Сотрудники', on_click=show_users, icon='logout')
#         ui.button('Оборудование', on_click=show_equip, icon='logout')
#         ui.button('Оффис', on_click=show_office, icon='logout')
#


@ui.page('/office')
def office():
    with ui.row().classes('w-full center-buttons').style(
            'display: flex; justify-content: center;'
    ):
        ui.button('Сотрудники', on_click=lambda: ui.navigate.to('/main'))
        ui.button('Оборудование', on_click=lambda: ui.navigate.to('/equip'))
        ui.button('Офисы', on_click=lambda: ui.navigate.to('/office'))
    m = ui.leaflet(center=(51.505, -0.09))
    ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.3f}, {center[1]:.3f}')
    ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')
    with ui.grid(columns=5, rows=5).classes("absolute-center").style('display: flex; justify-content: center;'):
        ui.button('Ставрополь', on_click=lambda: m.set_center((45.045361, 41.969658)))
        ui.button('Майкоп', on_click=lambda: m.set_center((44.610072, 40.108897)))
        ui.button('Таганрог', on_click=lambda: m.set_center((47.217096, 38.918207)))
        ui.button('Новочеркасск', on_click=lambda: m.set_center((47.420961, 40.097605)))
        ui.button('Шахты', on_click=lambda: m.set_center((47.708267, 40.211485)))
    with ui.grid(columns=2, rows=5).classes("items-center").style('display: flex; justify-content: center;'):
        ui.button(icon='zoom_in', on_click=lambda: m.set_zoom(m.zoom + 1))
        ui.button(icon='zoom_out', on_click=lambda: m.set_zoom(m.zoom - 1))


@ui.page('/equip')
def equip():

    with ui.row().classes('w-full center-buttons').style(
        'display: flex; justify-content: center;'
    ):
        ui.button('Сотрудники', on_click=lambda: ui.navigate.to('/main'))
        ui.button('Оборудование', on_click=lambda: ui.navigate.to('/equip'))
        ui.button('Офисы', on_click=lambda: ui.navigate.to('/office'))

    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()



    columns = [
        {'name': 'name', 'label': 'Название', 'field': 'name', 'required': True},
        {'name': 'number', 'label': 'Серийный номер', 'field': 'number', 'sortable': True},
        {'name': 'status', 'label': 'Статус', 'field': 'status', 'sortable': True},
        {'name': 'owner', 'label': 'Ответственный', 'field': 'owner', 'sortable': True},
        {'name': 'office', 'label': 'Офис', 'field': 'office', 'sortable': True},
    ]

    ui.button('Обновить', on_click=lambda: update_equip(table))
    with ui.table(title='Оборудование', columns=columns, rows=func_equip(), selection='multiple', pagination=8).classes('w-105 absolute-center') as table:


        with table.add_slot('top-right'):
            with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
        with table.add_slot('bottom-row'):
            with table.cell():
                name = ui.input('Название')
            with table.cell():
                number = ui.input('Серийный номер')
            with table.cell():
                status = ui.input('Статус')
            with table.cell():
                owner = ui.input('Ответственный')
            with table.cell():
                office = ui.input('Офис')
            ui.button(on_click=lambda: reg_equip(name, number, status, owner, office, table), icon='add').props('flat fab-mini')
    ui.button('Удалить', on_click=lambda: delete_equip(table.selected, table)) \
        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

def reg_equip(name, number, status, owner, office, table):
    name = name.value
    number = number.value
    status = status.value
    owner = owner.value
    office = office.value
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    try:
        cursor.execute("SELECT number FROM equipment WHERE number = ?", [number])
        if cursor.fetchone() is None:
            values = [name, number, status, owner, office]
            cursor.execute("INSERT INTO equipment(name, number, status, owner, office) VALUES(?, ?, ?, ?, ?)", values)
            ui.notify('Данные добавлены',color='positive')
            db.commit()
            update_equip(table)
        else:
            ui.notify("Данное оборудование уже учтено", color='negative')

    except sqlite3.Error as e:
        ui.notify(f'Ошибка базы данных: {e}')
    finally:
        cursor.close()
        db.close()
        func_equip()

def update_equip(table):
    table.rows=func_equip()
    table.update()
    ui.notify('Таблица успешко обновлена', color='positive')
def func_equip():
    dp = sqlite3.connect("database.db")
    cursor = db.cursor()
    a = []
    for i in cursor.execute("SELECT * FROM equipment"):
        new_dict = {'id': i[0], 'name': i[1], 'number': i[2], 'status': i[3], 'owner': i[4], 'office': i[5]}
        a.append(new_dict)
    cursor.close()
    dp.close()
    return a



def delete_equip(val,table):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    for i in val:
        user_id = i['id']
        try:
            cursor.execute(f"DELETE from equipment where `id` = ?", [user_id])
            db.commit()
            ui.notify("Запись успешно удалена", color='positive')
            update_equip(table)
        except sqlite3.Error as e:
            ui.notify(f'Ошибка базы данных: {e}')
        finally:
            print('ooooooo')


@ui.page('/main')
def main():

    with ui.row().classes('w-full center-buttons').style(
        'display: flex; justify-content: center;'
    ):
        ui.button('Сотрудники', on_click=lambda: ui.navigate.to('/main'))
        ui.button('Оборудование', on_click=lambda: ui.navigate.to('/equip'))
        ui.button('Офисы', on_click=lambda: ui.navigate.to('/office'))


    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()



    columns = [
        {'name': 'name', 'label': 'Имя', 'field': 'name', 'required': True},
        {'name': 'surname', 'label': 'Фамилия', 'field': 'surname', 'sortable': True},
        {'name': 'age', 'label': 'Возраст', 'field': 'age', 'sortable': True},
        {'name': 'work', 'label': 'Должность', 'field': 'work', 'sortable': True},
        {'name': 'office', 'label': 'Офис', 'field': 'office', 'sortable': True},
    ]

    ui.button('Обновить', on_click=lambda: update(table)).classes('')
    with ui.table(title='Сотрудники', columns=columns, rows=func(), selection='multiple', pagination=8).classes('w-105 absolute-center') as table:


        with table.add_slot('top-right'):
            with ui.input(placeholder='Поиск').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
        with table.add_slot('bottom-row'):
            with table.cell():
                name = ui.input('Имя')
            with table.cell():
                surname = ui.input('Фамилия')
            with table.cell():
                date = ui.input('Возраст')
            with table.cell():
                work = ui.input('Должность')
            with table.cell():
                office = ui.input('Офис')
            ui.button(on_click=lambda: reg_user(name, surname, date, work, office, table), icon='add').props('flat fab-mini')
    ui.button('Удалить', on_click=lambda: delete_users(table.selected, table)) \
        .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

def reg_user(name, surname, date, work, office, table):
    name = name.value
    surname = surname.value
    date = date.value
    work = work.value
    office = office.value
    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    try:
        cursor.execute("SELECT name and surname FROM users WHERE name = ? and surname = ?", [name, surname])
        if cursor.fetchone() is None:
            values = [name, surname, date, work, office]
            cursor.execute("INSERT INTO users(name, surname, age, work, office) VALUES(?, ?, ?, ?, ?)", values)
            ui.notify('Данные добавлены',color='positive')
            db.commit()
            update(table)
        else:
            ui.notify("Такой сотрудник уже есть", color='negative')

    except sqlite3.Error as e:
        ui.notify(f'Ошибка базы данных: {e}')
    finally:
        cursor.close()
        db.close()
        func()
def update(table):
    table.rows=func()
    table.update()
    ui.notify('Таблица успешко обновлена', color='positive')
def func():
    dp = sqlite3.connect("database.db")
    cursor = db.cursor()
    a = []
    for i in cursor.execute("SELECT * FROM users"):
        new_dict = {'id': i[0], 'name': i[1], 'surname': i[2], 'age': i[3], 'work': i[4], 'office': i[5]}
        a.append(new_dict)
    cursor.close()
    dp.close()
    return a
def delete_users(val,table):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    for i in val:
        user_id = i['id']
        try:
            cursor.execute(f"DELETE from users where `id` = ?", [user_id])
            db.commit()
            ui.notify("Запись успешно удалена", color='positive')
            update(table)
        except sqlite3.Error as e:
            ui.notify(f'Ошибка базы данных: {e}')
        finally:
            print('ooooooo')
ui.run()
webbrowser.open('http://localhost:8080/')
